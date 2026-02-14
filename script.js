const countries = document.getElementsByClassName('country-path'); 

// Extract country data

const dataHeaders = [
    'Code','Rank','True Rank','Entity','Instances','Accuracy','Value',
    'airPollution','co2PerCapita','debtToGdp','democracyIndex','drugUse',
    'education','fertility','gdpPerCapita','happiness','lifeExpectancy',
    'literacy','smoking','territoryControl','topOneIncome','topTenIncome',
    'waterSanitationHygiene','womensCivilRights','corruption','freedom','undernourishment'
];
const stringHeaders = ['Code', 'Entity'];

let allCountryData = {}
let scoreList = []

for (let n = 0; n < countries.length; n++) {
    let pathElement = countries[n]
    let rawData = pathElement.getAttribute('data-stats')
    let dataList = rawData.split(',')

    let countryData = {}

    for (let d = 0; d < dataHeaders.length; d++) {
        let thisHeader = dataHeaders[d];
        let dataPoint = dataList[d];

        if (dataPoint == '') {
            // Data point DNE
            dataPoint = null;
        } else if (!stringHeaders.includes(thisHeader)) {
            // Data point is numerical
            dataPoint = Number(dataPoint)
        }

        if (thisHeader == 'Value') scoreList.push(dataPoint);

        countryData[thisHeader] = dataPoint;
    }

    allCountryData[pathElement.id] = countryData;
}

console.log(allCountryData)


// Finding min and max

let cleansedScoreList = scoreList.filter(a => a != null)

const maxScore = Math.max(...cleansedScoreList);
const minScore = Math.min(...cleansedScoreList);

console.log(minScore, maxScore)

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
    let pathElement = countries[n];
    let countryData = allCountryData[pathElement.id];

    if (!pathElement.classList.contains('no-data')) {
        let rawScore = countryData['Value'];
        
        // Normalize score
        let score = interpolate(rawScore, minScore, maxScore, 0, 1)

        // Find color stop indexes
        let colorStartIndex;
        let colorEndIndex;

        for (let i = 0; i < colorStops.length; i++) {
            let percentage = colorStops[i][0];

            if (score < percentage || i == colorStops.length - 1) {
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
        
        pathElement.style.fill = `hsl(
            ${finalColorData[0]}, 
            ${finalColorData[1]}%, 
            ${finalColorData[2]}%
        )`;

    }

    // End of check for no-data class

    pathElement.addEventListener('mouseover', (e) => {
        // document.getElementById('z-index-override').setAttribute("href", `#${countryData['Code']}`);3
    })

    pathElement.addEventListener('mouseenter', (e) => {
        currentlyHoveringOverCode = countryData['Code'];
        updateTooltip();
    })
    pathElement.addEventListener('mouseout', (e) => {
        currentlyHoveringOverCode = '';

        if (countryData['Code'] == currentlyHoveringOverCode) {
            currentlyHoveringOverCode = '';
        }
        updateTooltip()
    })
}



// Tooltip movement

let currentlyHoveringOverCode = '';

const tooltip = document.getElementById('tooltip');
const tooltipText = document.getElementById('tooltip-text');
const mapContainer = document.getElementById('map-container');

mapContainer.addEventListener('mousemove', (e) => {
    tooltip.style.top = `${e.clientY - 10}px`;
    tooltip.style.left = `${e.clientX + 20}px`;
})

// Tooltip naming

function updateTooltip() {
    let hoverCodeExists = (currentlyHoveringOverCode != '');

    tooltip.style.display = hoverCodeExists ? 'block' : 'none';

    if (currentlyHoveringOverCode != '') {
        let countryData = allCountryData[currentlyHoveringOverCode];

        tooltipText.innerHTML = `${countryData['Entity']} <span id="country-value">${Math.round(countryData['Value'] * 10)/10}</span>`;
        document.getElementById('value-progress').style.backgroundColor = document.getElementById(countryData['Code']).style.fill;
        document.getElementById('value-progress').style.width = `${countryData['Value']}%`;
    }
}
