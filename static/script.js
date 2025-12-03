// Update character count
document.getElementById('reviewInput').addEventListener('input', function() {
    const charCount = this.value.length;
    document.getElementById('charCount').textContent = charCount;
    
    
    if (charCount > 10000) {
        this.value = this.value.substring(0, 10000);
        document.getElementById('charCount').textContent = '10000';
    }
});


async function analyzeReview() {
    const reviewText = document.getElementById('reviewInput').value.trim();
    
    
    if (!reviewText) {
        showError('Please enter a review');
        return;
    }
    
    if (reviewText.length < 10) {
        showError('Review must be at least 10 characters long');
        return;
    }
    
    hideError();
    hideResults();
    showLoading();
    
    try {
        const response = await fetch('/predict', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ review: reviewText })
        });
        
        const data = await response.json();
        
        if (!response.ok) {
            showError(data.error || 'An error occurred');
            hideLoading();
            return;
        }
        
        
        displayResults(data);
        hideLoading();
        
    } catch (error) {
        showError('Failed to analyze review. Please try again.');
        hideLoading();
        console.error('Error:', error);
    }
}


function displayResults(data) {
    const sentiment = data.sentiment;
    const confidence = data.confidence;
    const rating = data.rating;
    
    
    const badge = document.getElementById('sentimentBadge');
    badge.textContent = sentiment === 'Positive' ? '✓' : '✗';
    badge.className = `sentiment-badge ${sentiment.toLowerCase()}`;
    
    
    document.getElementById('sentimentResult').textContent = sentiment;
    document.getElementById('ratingResult').textContent = rating + '/10';
    document.getElementById('confidenceResult').textContent = (confidence * 100).toFixed(1) + '%';
    
    
    const fill = document.getElementById('confidenceFill');
    fill.style.width = (confidence * 100) + '%';
    
    
    displayStars(rating);
    
    
    showResults();
}


function displayStars(rating) {
    const fullStars = Math.floor(rating);
    const hasHalfStar = rating % 1 >= 0.5;
    let stars = '';
    
    for (let i = 0; i < fullStars; i++) {
        stars += '★';
    }
    
    if (hasHalfStar && fullStars < 10) {
        stars += '½';
    }
    
    
    const emptyStars = 10 - Math.ceil(rating);
    for (let i = 0; i < emptyStars; i++) {
        stars += '☆';
    }
    
    document.getElementById('starsDisplay').textContent = stars;
}


function showResults() {
    document.getElementById('resultsContainer').style.display = 'block';
    
    document.getElementById('resultsContainer').scrollIntoView({ behavior: 'smooth', block: 'nearest' });
}

function hideResults() {
    document.getElementById('resultsContainer').style.display = 'none';
}

function showError(message) {
    const errorContainer = document.getElementById('errorContainer');
    document.getElementById('errorMessage').textContent = message;
    errorContainer.style.display = 'block';
}

function hideError() {
    document.getElementById('errorContainer').style.display = 'none';
}

function showLoading() {
    document.getElementById('loadingContainer').style.display = 'block';
}

function hideLoading() {
    document.getElementById('loadingContainer').style.display = 'none';
}

document.getElementById('reviewInput').addEventListener('keydown', function(e) {
    if ((e.ctrlKey || e.metaKey) && e.key === 'Enter') {
        analyzeReview();
    }
});

// Example reviews for testing
const exampleReviews = [
    "This movie was absolutely fantastic! The cinematography was stunning, the plot kept me engaged throughout, and the acting performances were superb. I laughed, I cried, and I was on the edge of my seat. Definitely a masterpiece that I will watch again and again!",
    "Terrible waste of time. The story made no sense, the characters were poorly developed, and the acting was cringe-worthy. I couldn't even finish watching it. Save your money and watch something else instead."
];

function loadExampleReview() {
    const review = exampleReviews[Math.floor(Math.random() * exampleReviews.length)];
    document.getElementById('reviewInput').value = review;
    document.getElementById('charCount').textContent = review.length;
}
