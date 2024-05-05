document.getElementById('nameForm').addEventListener('submit', function(event) {
    event.preventDefault(); // Stop the form from submitting normally
    const keyword = document.getElementById('keywordInput').value;
    const numResults = document.getElementById('numResults').value || 5; // Default to 5 names if not specified
    
    
    // Show the results container
    document.getElementById('resultsContainer').style.display = 'block';


    fetchNames(keyword, numResults);
});


function fetchNames(keyword, numResults) {
    fetch('/generate', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            keywords: keyword,
            num_suggestions: numResults
        })
    })
    .then(response => response.json())
    .then(data => {
        const list = document.getElementById('nameList');
        list.innerHTML = ''; // Clear existing names
        data.forEach(name => {
            const listItem = document.createElement('li');
            listItem.textContent = name;
            list.appendChild(listItem);
        });
    })
    .catch(error => console.error('Error fetching names:', error));
}


function createBubble() {
    const bubble = document.createElement('div');
    bubble.classList.add('bubble');
    document.body.appendChild(bubble);

    // Randomize the size and animation duration to make it more natural
    const size = Math.random() * 95 + 5; // Bubble size between 5 and 100 pixels
    bubble.style.width = `${size}px`;
    bubble.style.height = `${size}px`;

    // Adjust left positioning to prevent overflow
    let leftPosition = Math.random() * 100;
    leftPosition = Math.min(leftPosition, 100); // Keep within 5% to 95% to avoid horizontal scroll
    bubble.style.left = `${leftPosition}%`;

    // Randomize the speed of the animation
    const duration = Math.random() * 5 + 8; // Duration between 8 and 13 seconds
    bubble.style.animationDuration = `${duration}s`;

    // Remove the bubble after it finishes animating to avoid cluttering the DOM
    bubble.addEventListener('animationend', function() {
        bubble.remove();
    });
}

// Create a new bubble every half second
setInterval(createBubble, 500);
