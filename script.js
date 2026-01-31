const countries = document.getElementsByClassName('country-path'); 

// Finding min and max

scoreList = []

for (let n = 0; n < countries.length; n++) {
    path = countries[n]
    score = parseFloat(path.getAttribute('data-score'))
    if (score > 0) { scoreList.push(score) }
}

const maxScore = Math.max(...scoreList);
const minScore = Math.min(...scoreList);

// Interpolation function

function interpolate(x, a1, a2, b1, b2) {
    return (b2 - b1) * (x - a1) / (a2 - a1) + b1
}

// Coloring

for (let n = 0; n < countries.length; n++) {
    path = countries[n]
    rawScore = parseFloat(path.getAttribute('data-score'))
    
    // Normalize score
    score = interpolate(rawScore, minScore, maxScore, 0, 1)

    path.style.fill = `hsl(
        ${score*230}, 
        70%, 
        50%
    )`
}