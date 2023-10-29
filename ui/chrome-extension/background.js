chrome.runtime.onMessage.addListener(function (request, sender, sendResponse) {
  if (request.action === 'queryAiModel') {
    console.log('Querying the AI model API...');
    fetch('http://127.0.0.1:5000/predict', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({sentences: request.sentences, questions: request.questions}),
    })
    .then(response => response.json())
    .then(data => {
      sendResponse({ data: data });
    })
    .catch(error => {
      console.error('There was an error!', error);
      sendResponse({ error: error.toString() });
    });

    return true;
  }
});
