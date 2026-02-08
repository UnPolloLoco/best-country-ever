const countries = document.getElementsByClassName('country-path'); 

// Extract country data

for (let n = 0; n < countries.length; n++) {
    let path = countries[n]
    let rawData = path.getAttribute('data-stats')
    let dataList = rawData.split(',')
}

// Finding min and max

// scoreList = []

// for (let n = 0; n < countries.length; n++) {
//     path = countries[n]
//     score = parseFloat(path.getAttribute('data-score'))
//     if (score > 0) { scoreList.push(score) }
// }

// const maxScore = Math.max(...scoreList);
// const minScore = Math.min(...scoreList);

const maxScore = 88;
const minScore = 26;

// Interpolation function

function interpolate(x, a1, a2, b1, b2) {
    let val = (b2 - b1) * (x - a1) / (a2 - a1) + b1;
    let outMin = Math.min(b1, b2);
    let outMax = Math.max(b1, b2);

    return Math.min(Math.max(val, outMin), outMax);
}

// Color variations

const colorStops = [
    [
        [0.00, [60,  90, 90]],
        [0.35, [45,  90, 50]],
        [0.50, [25,  90, 50]],
        [0.65, [0,   70, 50]],
        [1.00, [-60, 70, 15]],
    ],
    [
        [0.00, [180, 70, 95]], 
        [0.50, [200, 70, 60]],
        [1.00, [225, 70, 35]],
    ]
][1]

// Country loop

for (let n = 0; n < countries.length; n++) {
    setTimeout(() => {
        let path = countries[n]
        let rawData = path.getAttribute('data-stats')
        let dataList = rawData.split(',')

        let rawScore = parseFloat(dataList[6]);
        
        // Normalize score
        let score = interpolate(rawScore, minScore, maxScore, 0, 1)

        // Find color stop indexes
        let colorStartIndex;
        let colorEndIndex;

        for (let i = 0; i < colorStops.length; i++) {
            let percentage = colorStops[i][0];

            if (score < percentage) {
                colorStartIndex = i - 1;
                colorEndIndex = i;
                break;
            }
        }

        // Find dist between stops

        let progressBetweenStops = interpolate(
            score, 
            colorStops[colorStartIndex][0], colorStops[colorEndIndex][0], 
            0, 1
        );

        // Interpolate colors

        let colorStart = colorStops[colorStartIndex][1];
        let colorEnd = colorStops[colorEndIndex][1];

        let finalColorData = []
        for (let i = 0; i < 3; i++) {
            // Loop through H, S, L
            let thisStart = colorStart[i];
            let thisEnd = colorEnd[i];

            finalColorData.push(interpolate(
                progressBetweenStops,
                0, 1,
                thisStart, thisEnd,
            ))
        }

        
        // Fill color
        
        path.style.fill = `hsl(
            ${finalColorData[0]}, 
            ${finalColorData[1]}%, 
            ${finalColorData[2]}%
        )`;

        path.onmouseover = (() => {
            document.getElementById('country-name').innerText = dataList[3];
            document.getElementById('z-index-override').setAttribute("href", `#${dataList[0]}`);
        })

    }, 1000*Math.random())
}


// Tooltip

let tooltip = document.getElementById('country-name');
document.body.onmousemove = ((e) => {
    tooltip.style.top = `${e.clientY}px`;
    tooltip.style.left = `${e.clientX}px`;
})

