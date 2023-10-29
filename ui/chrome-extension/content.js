console.log('content.js active...')

function isVisible(element) {
  const style = window.getComputedStyle(element);
  const isHidden = style.display === 'none' || style.visibility === 'hidden' || style.opacity === '0';
  return !isHidden;
}

function extractVisibleText(node) {
  let text = '';
  if (node.nodeType === Node.TEXT_NODE && isVisible(node.parentNode)) {
    text += node.textContent.trim() + ' ';
  } else if (node.nodeType === Node.ELEMENT_NODE) {
    for (const child of node.childNodes) {
      text += extractVisibleText(child);
    }
  }
  return text;
}

function splitText(text) {
    return text.split(/(?<=[.!?])\s+/);
}

function chunkText(text, chunkSize) {
    let chunk = [], chunks = [], currentLength = 0;
    for (let sentence of splitText(text)) {
        if (currentLength + sentence.length > chunkSize && currentLength > 0) {
            chunks.push(chunk);
            chunk = [];
            currentLength = 0;
        }
        if (sentence.length <= chunkSize) {
            chunk.push(sentence);
            currentLength += sentence.length;
        }
    }

    if (currentLength) chunks.push(chunk);
    return chunks;
}

chrome.runtime.onMessage.addListener(function (request, sender, sendResponse) {
  if (request.action === 'analyze') {
    let chunks = chunkText(extractVisibleText(document.body), 512);
    chrome.runtime.sendMessage({action: 'expectedResults', chunksCount: chunks.length});
    chunks.forEach(sentences => {
        chrome.runtime.sendMessage(
          {
             action: 'queryAiModel',
             sentences,
             questions: request.questions
          },
          function (response) {
            if (response.error) {
              console.error(response.error);
            }

            const text = response.data.length > 0 ? response.data.join("") : '';
            chrome.runtime.sendMessage({action: 'results', text: text});
          }
        );
    });
  }
});
