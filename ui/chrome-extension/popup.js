console.log("popup.js active...");

document.addEventListener('DOMContentLoaded', function () {
    let expectedResults = 0, receivedResults = 0;
    const questionsContainer = document.getElementById('questions-container');
    const resultsContainer = document.getElementById('results-container');

    const addQuestionButton = document.getElementById('add-question-button');
    const getResultsButton = document.getElementById('get-results-button');
    const clearResultsButton = document.getElementById('clear-results-button');

    const loadingSpinner = document.getElementById('custom-spinner-container');

    addQuestionButton.addEventListener('click', () => {
        const questionDiv = document.createElement('div');
        questionDiv.className = 'question';

        const textField = document.createElement('input');
        textField.type = 'text';
        textField.className = 'mdc-text-field__input';

        const deleteButton = document.createElement('button');
        deleteButton.className = 'delete-button mdc-button mdc-button--raised mdc-button--dense';
        deleteButton.innerHTML = 'Delete';
        deleteButton.addEventListener('click', () => {
            questionsContainer.removeChild(questionDiv);
            if (questionsContainer.children.length === 0) {
                sendButton.disabled = true;
            }
        });

        questionDiv.appendChild(textField);
        questionDiv.appendChild(deleteButton);
        questionsContainer.appendChild(questionDiv);
        getResultsButton.disabled = false;
    });

    getResultsButton.addEventListener('click', function () {
        resultsContainer.innerText = "";
        const inputs = questionsContainer.getElementsByTagName('input');
        let questions = [];
        for (let input of inputs) {
            questions.push(input.value);
        }

        expectedResults = 0;
        receivedResults = 0;
        chrome.tabs.query({ active: true, currentWindow: true }, function (tabs) {
            chrome.tabs.sendMessage(tabs[0].id, { action: 'analyze', questions });
        });
    });

    clearResultsButton.addEventListener('click', function () {
        resultsContainer.innerText = "";
        clearResultsButton.disabled = true;
    });

    chrome.runtime.onMessage.addListener(function (request, sender, sendResponse) {
        if (request.action === 'results') {
            receivedResults ++;
            resultsContainer.innerText += request.text;

            if (receivedResults == expectedResults) {
                clearResultsButton.disabled = false;
                loadingSpinner.className = 'hide';
            }
        }

        if (request.action === 'expectedResults') {
            expectedResults = request.chunksCount;
            loadingSpinner.className = '';
        }
    });
});


