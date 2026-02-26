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



// Finding min and max

let cleansedScoreList = scoreList.filter(a => a != null)

const maxScore = Math.max(...cleansedScoreList);
const minScore = Math.min(...cleansedScoreList);

// Interpolation function

function interpolate(x, a1, a2, b1, b2) {
    let val = (b2 - b1) * (x - a1) / (a2 - a1) + b1;
    let outMin = Math.min(b1, b2);
    let outMax = Math.max(b1, b2);

    return Math.min(Math.max(val, outMin), outMax);
}

// Score normalizer

function normalizeScore(x) {
    return interpolate(x, minScore, maxScore, 0, 1);
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

// Color-from-value function

function getColor(x) {
    // Normalize
    let score = normalizeScore(x);

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

    return finalColorData;
}

// Country loop

const zIndexOverride = document.getElementById('z-index-override');

for (let n = 0; n < countries.length; n++) {
    let pathElement = countries[n];
    let countryData = allCountryData[pathElement.id];

    // Fill color

    if (!pathElement.classList.contains('no-data')) {
        let score = countryData['Value'];
        let finalColorData = getColor(score);
        
        pathElement.style.fill = `hsl(
            ${finalColorData[0]}, 
            ${finalColorData[1]}%, 
            ${finalColorData[2]}%
        )`;

    }

    // End of check for no-data class

    pathElement.addEventListener('mouseover', (e) => {
        let pathData = e.target.getAttribute('d');
        zIndexOverride.setAttribute("d", pathData);
    })

    pathElement.addEventListener('mouseenter', (e) => {
        currentlyHoveringOverCode = countryData['Code'];
        updateHoverEffects(e.target);
    })
    pathElement.addEventListener('mouseout', (e) => {
        currentlyHoveringOverCode = '';
        updateHoverEffects(e.target);
    })
}



// Tooltip movement

let currentlyHoveringOverCode = '';

const tooltip = document.getElementById('tooltip');
const tooltipLabel = document.getElementById('tooltip-text');
const tooltipScore = document.getElementById('tooltip-score');
const mapContainer = document.getElementById('map-container');

let hasMovedMouse = false;

mapContainer.addEventListener('mousemove', (e) => {
    tooltip.style.top = `${e.clientY}px`;
    tooltip.style.left = `${e.clientX + 15}px`;

    hasMovedMouse = true;
})

// Tooltip updates

function updateHoverEffects(target) {
    let hoverCodeExists = (currentlyHoveringOverCode != '');
    let showHoverEffects = (hoverCodeExists && hasMovedMouse);

    let data = allCountryData[target.id];
    let score = data['Value'];

    let mainColor;
    let shadowColor;

    // let tooltipLabelText;
    let tooltipScoreText;

    if (currentlyHoveringOverCode != '') {

        // --------- SCORE EXISTS? --------- 
        if (score) {

            // Normalize Score
            let normScore = normalizeScore(score);
            let inverseNormScore = 1 - normScore;

            // Text
            tooltipScoreText = score.toFixed(1);
    
            // Score coloring
    
            let mainColorData = getColor(score);
            let finalBrightness = Math.max(67, mainColorData[2]);
    
            mainColor = `hsl(
                ${mainColorData[0]}, 
                100%, 
                ${finalBrightness}%
            )`;
    
            shadowColor = `hsl(
                ${mainColorData[0] + 10}, 
                ${64 - 10*inverseNormScore}%, 
                ${52 - 10*inverseNormScore}%
            )`;
        
        // --------- SCORE DOESNT EXIST? --------- 

        } else {
            tooltipScoreText = '<span id="no-data-first-dash">–</span>–.–';
            mainColor = '#888';
            shadowColor = '#555';
        }


        
        
        // Tooltip text
        tooltipLabel.innerText = data['Entity'];
        tooltipScore.innerHTML = tooltipScoreText;

        // Tooltip colors
        tooltipScore.style.color = mainColor;
        tooltipScore.style.textShadow = `0 3px 0 ${shadowColor}`;
    }

    // Tooltip display
    tooltip.style.display = showHoverEffects ? 'flex' : 'none';
    zIndexOverride.style.display = showHoverEffects ? '' : 'none';

    // Low/no data indicator

    let isLowData = target.classList.contains('low-data');
    let isNoData = target.classList.contains('no-data');

    const tnContainer = document.getElementById('tooltip-notice-flex');
    const tnText = document.getElementById('tooltip-notice');

    if (isLowData) {
        // Low data
        tnContainer.style.display = 'flex';
        tnText.style.color = 'var(--low-data-color)';
        tnText.innerText = 'Low Data';
    } else if (isNoData) {
        // No data
        tnContainer.style.display = 'flex';
        tnText.style.color = 'var(--no-data-color)';
        tnText.innerText = 'No Data';
    } else {
        // Sufficient data
        tnContainer.style.display = 'none';
    }
}
