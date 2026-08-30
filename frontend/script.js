const API_URL = "http://127.0.0.1:8000";

/* =========================================================
   DOM ELEMENTS
========================================================= */

const predictionForm = document.getElementById("predictionForm");
const predictButton = document.getElementById("predictButton");

const result = document.getElementById("result");
const resultSection = document.getElementById("resultSection");
const depreciationChart = document.getElementById("depreciationChart");

const brandSelect = document.getElementById("brand");
const modelSelect = document.getElementById("model");
const engineSelect = document.getElementById("engine_cc");

const ageInput = document.getElementById("age_months");
const kmInput = document.getElementById("km_driven");
const ownersSelect = document.getElementById("owners");
const conditionSelect = document.getElementById("condition");
const launchPriceInput = document.getElementById("launch_price");

const selectedBikeImage = document.getElementById("selectedBikeImage");


/* =========================================================
   STATE
========================================================= */

/*
 * IMPORTANT:
 *
 * The image is NOT loaded when the user selects a model.
 *
 * It is loaded ONLY after a successful prediction.
 */

let currentBikeImage = "";

const bikeImageCache = new Map();


/* =========================================================
   FALLBACK IMAGE
========================================================= */

/*
 * This is NOT shown initially.
 *
 * It is only used if Wikimedia cannot find an image
 * for the analysed bike.
 */

const FALLBACK_BIKE_IMAGE =
    "https://images.unsplash.com/photo-1558981806-ec527fa84c39?q=80&w=1200&auto=format&fit=crop";


/* =========================================================
   IMAGE VISIBILITY
========================================================= */

/*
 * Hide the image.
 *
 * Called when:
 * - page loads
 * - new model is selected
 * - prediction starts
 * - prediction fails
 */

function hideBikeImage() {

    if (!selectedBikeImage) {
        return;
    }

    selectedBikeImage.removeAttribute("src");

    selectedBikeImage.alt = "";

    selectedBikeImage.style.display = "none";
}


/*
 * Show the image.
 */

function showBikeImage(imageUrl, brand, model) {

    if (!selectedBikeImage) {
        console.warn(
            "selectedBikeImage element was not found in index.html."
        );

        return;
    }

    if (!imageUrl) {
        hideBikeImage();
        return;
    }

    selectedBikeImage.src = imageUrl;

    selectedBikeImage.alt =
        `${brand} ${model}`;

    selectedBikeImage.style.display = "block";
}


/* =========================================================
   CREATE IMAGE SEARCH KEY
========================================================= */

function createBikeImageKey(brand, model) {

    return `${brand.trim().toLowerCase()}|${model.trim().toLowerCase()}`;
}


/* =========================================================
   LOCAL IMAGE MAPPING
========================================================= */

/*
 * You can place exact images in:
 *
 * images/bikes/
 *
 * Example:
 *
 * images/bikes/honda-activa-125.jpg
 * images/bikes/honda-shine.jpg
 * images/bikes/hero-splendor.jpg
 *
 * If an exact image exists here, it will be used first.
 *
 * Otherwise Wikimedia Commons will be searched.
 */

function getLocalBikeImage(brand, model) {

    const key =
        createBikeImageKey(
            brand,
            model
        );

    const bikeImages = {

        /*
         * EXAMPLES
         *
         * Uncomment and add your own files.
         */

        /*
        "honda|activa 125":
            "images/bikes/honda-activa-125.jpg",

        "honda|shine":
            "images/bikes/honda-shine.jpg",

        "hero|splendor":
            "images/bikes/hero-splendor.jpg",

        "bajaj|pulsar 150":
            "images/bikes/bajaj-pulsar-150.jpg",

        "yamaha|r15":
            "images/bikes/yamaha-r15.jpg",

        "royal enfield|classic 350":
            "images/bikes/royal-enfield-classic-350.jpg",

        "ktm|duke 200":
            "images/bikes/ktm-duke-200.jpg"
        */

    };

    return bikeImages[key] || null;
}


/* =========================================================
   SEARCH WIKIMEDIA COMMONS
========================================================= */

/*
 * Wikimedia Commons provides publicly accessible images.
 *
 * We search ONLY after the prediction succeeds.
 *
 * This means image searching can never stop the prediction.
 */

async function searchWikimediaBikeImage(
    brand,
    model
) {

    const query =
        `${brand} ${model} motorcycle`;

    const params =
        new URLSearchParams({

            action: "query",

            generator: "search",

            gsrsearch: query,

            gsrnamespace: "6",

            gsrlimit: "5",

            prop: "imageinfo",

            iiprop: "url",

            iiurlwidth: "1000",

            format: "json",

            origin: "*"

        });


    try {

        const response =
            await fetch(
                `https://commons.wikimedia.org/w/api.php?${params.toString()}`
            );


        if (!response.ok) {

            throw new Error(
                "Wikimedia image search failed."
            );
        }


        const data =
            await response.json();


        const pages =
            data?.query?.pages;


        if (!pages) {
            return null;
        }


        const pageList =
            Object.values(pages);


        /*
         * Find the first usable image.
         */

        for (
            const page
            of pageList
        ) {

            const imageInfo =
                page?.imageinfo?.[0];


            if (!imageInfo) {
                continue;
            }


            const imageUrl =
                imageInfo.thumburl ||
                imageInfo.url;


            if (imageUrl) {

                return imageUrl;
            }
        }


    } catch (error) {

        console.warn(
            "Bike image search failed:",
            error
        );

    }


    return null;
}


/* =========================================================
   GET BIKE IMAGE
========================================================= */

async function getBikeImage(
    brand,
    model
) {

    if (!brand || !model) {
        return null;
    }


    const key =
        createBikeImageKey(
            brand,
            model
        );


    /*
     * Check cache.
     */

    if (
        bikeImageCache.has(key)
    ) {

        return bikeImageCache.get(key);
    }


    /*
     * First check local exact images.
     */

    const localImage =
        getLocalBikeImage(
            brand,
            model
        );


    if (localImage) {

        bikeImageCache.set(
            key,
            localImage
        );

        return localImage;
    }


    /*
     * Otherwise search Wikimedia.
     */

    const onlineImage =
        await searchWikimediaBikeImage(
            brand,
            model
        );


    /*
     * If nothing is found, use fallback.
     */

    const finalImage =
        onlineImage ||
        FALLBACK_BIKE_IMAGE;


    bikeImageCache.set(
        key,
        finalImage
    );


    return finalImage;
}


/* =========================================================
   LOAD BIKE IMAGE AFTER PREDICTION
========================================================= */

async function loadBikeImageAfterPrediction(
    brand,
    model
) {

    if (
        !brand ||
        !model
    ) {

        hideBikeImage();

        return;
    }


    try {

        const imageUrl =
            await getBikeImage(
                brand,
                model
            );


        if (!imageUrl) {

            hideBikeImage();

            return;
        }


        currentBikeImage =
            imageUrl;


        showBikeImage(
            imageUrl,
            brand,
            model
        );


    } catch (error) {

        console.warn(
            "Could not load bike image:",
            error
        );


        hideBikeImage();
    }
}


/* =========================================================
   FORMAT INDIAN CURRENCY
========================================================= */

function formatCurrency(value) {

    const number =
        Number(value);


    if (
        !Number.isFinite(number)
    ) {

        return "₹0";
    }


    return new Intl.NumberFormat(
        "en-IN",
        {
            style: "currency",
            currency: "INR",
            maximumFractionDigits: 0
        }
    ).format(number);
}


/* =========================================================
   API ERROR MESSAGE
========================================================= */

async function getApiError(
    response,
    fallbackMessage
) {

    try {

        const errorData =
            await response.json();


        if (
            errorData?.detail
        ) {

            return errorData.detail;
        }


        if (
            errorData?.message
        ) {

            return errorData.message;
        }

    } catch (error) {

        console.warn(
            "Could not parse API error response."
        );
    }


    return fallbackMessage;
}


/* =========================================================
   SHOW ERROR
========================================================= */

function showError(message) {

    hideBikeImage();


    result.innerHTML = `

        <div class="result-icon">
            ⚠️
        </div>

        <div
            class="prediction-price"
            style="font-size: 24px;"
        >
            Prediction Failed
        </div>

        <p>
            ${message}
        </p>

    `;
}


/* =========================================================
   RESET ENGINE DROPDOWN
========================================================= */

function resetEngineDropdown(
    message = "Select Model First"
) {

    engineSelect.innerHTML = `

        <option value="">
            ${message}
        </option>

    `;

    engineSelect.disabled = true;
}


/* =========================================================
   RESET MODEL DROPDOWN
========================================================= */

function resetModelDropdown(
    message = "Select Brand First"
) {

    modelSelect.innerHTML = `

        <option value="">
            ${message}
        </option>

    `;

    modelSelect.disabled = true;
}


/* =========================================================
   BRAND CHANGE
========================================================= */

if (brandSelect) {

    brandSelect.addEventListener(
        "change",
        async function () {

            const brand =
                brandSelect.value;


            /*
             * IMPORTANT:
             *
             * Selecting another brand means
             * there is currently NO analysed bike.
             */

            hideBikeImage();

            currentBikeImage = "";


            resetModelDropdown(
                "Loading models..."
            );


            resetEngineDropdown();


            if (!brand) {

                resetModelDropdown(
                    "Select Brand First"
                );

                return;
            }


            try {

                const params =
                    new URLSearchParams({
                        brand: brand
                    });


                const response =
                    await fetch(
                        `${API_URL}/models?${params.toString()}`
                    );


                if (!response.ok) {

                    const message =
                        await getApiError(
                            response,
                            "Unable to load models for this brand."
                        );


                    throw new Error(
                        message
                    );
                }


                const data =
                    await response.json();


                if (
                    !Array.isArray(
                        data.models
                    ) ||
                    data.models.length === 0
                ) {

                    throw new Error(
                        "No models were found for this brand."
                    );
                }


                modelSelect.innerHTML = `

                    <option value="">
                        Select Model
                    </option>

                `;


                data.models.forEach(
                    model => {

                        const option =
                            document.createElement(
                                "option"
                            );


                        option.value =
                            model;


                        option.textContent =
                            model;


                        modelSelect.appendChild(
                            option
                        );

                    }
                );


                modelSelect.disabled = false;


            } catch (error) {

                console.error(
                    "Model loading error:",
                    error
                );


                resetModelDropdown(
                    "Could not load models"
                );


                showError(
                    error.message ||
                    "Could not load bike models."
                );
            }

        }
    );
}


/* =========================================================
   MODEL CHANGE
========================================================= */

if (modelSelect) {

    modelSelect.addEventListener(
        "change",
        async function () {

            const brand =
                brandSelect.value;


            const model =
                modelSelect.value;


            /*
             * IMPORTANT:
             *
             * DO NOT SHOW IMAGE HERE.
             *
             * The user has not analysed the bike yet.
             */

            hideBikeImage();

            currentBikeImage = "";


            resetEngineDropdown(
                "Loading engine capacity..."
            );


            if (
                !brand ||
                !model
            ) {

                resetEngineDropdown(
                    "Select Model First"
                );

                return;
            }


            try {

                const params =
                    new URLSearchParams({

                        brand:
                            brand,

                        model_name:
                            model

                    });


                const response =
                    await fetch(
                        `${API_URL}/engine?${params.toString()}`
                    );


                if (!response.ok) {

                    const message =
                        await getApiError(
                            response,
                            "Unable to load engine capacity."
                        );


                    throw new Error(
                        message
                    );
                }


                const data =
                    await response.json();


                if (
                    !Array.isArray(
                        data.engine_cc
                    ) ||
                    data.engine_cc.length === 0
                ) {

                    throw new Error(
                        "Engine capacity not found for this model."
                    );
                }


                engineSelect.innerHTML = `

                    <option value="">
                        Select Engine Capacity
                    </option>

                `;


                data.engine_cc.forEach(
                    cc => {

                        const option =
                            document.createElement(
                                "option"
                            );


                        option.value =
                            cc;


                        option.textContent =
                            `${cc} CC`;


                        engineSelect.appendChild(
                            option
                        );

                    }
                );


                /*
                 * Automatically select
                 * if only one engine exists.
                 */

                if (
                    data.engine_cc.length === 1
                ) {

                    engineSelect.value =
                        String(
                            data.engine_cc[0]
                        );
                }


                engineSelect.disabled = false;


            } catch (error) {

                console.error(
                    "Engine loading error:",
                    error
                );


                resetEngineDropdown(
                    "Engine capacity unavailable"
                );


                showError(
                    error.message ||
                    "Could not load engine capacity."
                );
            }

        }
    );
}


/* =========================================================
   DEPRECIATION CHART
========================================================= */

function createDepreciationChart(
    launchPrice,
    currentAge,
    predictedPrice
) {

    if (!depreciationChart) {
        return;
    }


    launchPrice =
        Number(launchPrice);


    currentAge =
        Number(currentAge);


    predictedPrice =
        Number(predictedPrice);


    if (
        !Number.isFinite(launchPrice) ||
        !Number.isFinite(currentAge) ||
        !Number.isFinite(predictedPrice)
    ) {

        return;
    }


    const maxAge =
        Math.max(
            60,
            Math.ceil(
                currentAge / 12
            ) * 12
        );


    const points = [];


    /*
     * Generate points every 6 months.
     */

    for (
        let age = 0;
        age <= maxAge;
        age += 6
    ) {

        let value;


        if (
            age <= currentAge
        ) {

            const progress =
                currentAge === 0
                    ? 0
                    : age / currentAge;


            value =
                launchPrice -
                (
                    (
                        launchPrice -
                        predictedPrice
                    ) *
                    progress
                );

        } else {

            const extraYears =
                (
                    age -
                    currentAge
                ) / 12;


            value =
                predictedPrice *
                Math.pow(
                    0.92,
                    extraYears
                );
        }


        value =
            Math.max(
                0,
                value
            );


        points.push({
            age: age,
            value: Math.round(value)
        });
    }


    /* =====================================================
       CHART DIMENSIONS
    ===================================================== */

    const width = 900;
    const height = 420;

    const paddingLeft = 80;
    const paddingRight = 40;
    const paddingTop = 40;
    const paddingBottom = 65;


    const chartWidth =
        width -
        paddingLeft -
        paddingRight;


    const chartHeight =
        height -
        paddingTop -
        paddingBottom;


    const maxValue =
        Math.max(
            launchPrice,
            ...points.map(
                point => point.value
            )
        );


    const minValue = 0;


    /* =====================================================
       X POSITION
    ===================================================== */

    function xPosition(age) {

        return (
            paddingLeft +
            (
                age /
                maxAge
            ) *
            chartWidth
        );
    }


    /* =====================================================
       Y POSITION
    ===================================================== */

    function yPosition(value) {

        if (
            maxValue === minValue
        ) {

            return (
                paddingTop +
                chartHeight / 2
            );
        }


        return (
            paddingTop +
            chartHeight -
            (
                (
                    value -
                    minValue
                ) /
                (
                    maxValue -
                    minValue
                )
            ) *
            chartHeight
        );
    }


    /* =====================================================
       LINE
    ===================================================== */

    const linePoints =
        points
            .map(
                point =>
                    `${xPosition(point.age)},${yPosition(point.value)}`
            )
            .join(" ");


    /* =====================================================
       AREA
    ===================================================== */

    const firstPoint =
        points[0];


    const lastPoint =
        points[
            points.length - 1
        ];


    const areaPoints = `

        ${xPosition(firstPoint.age)},${yPosition(0)}

        ${linePoints}

        ${xPosition(lastPoint.age)},${yPosition(0)}

    `;


    /* =====================================================
       CURRENT MARKER
    ===================================================== */

    const currentX =
        xPosition(
            Math.min(
                currentAge,
                maxAge
            )
        );


    const currentY =
        yPosition(
            predictedPrice
        );


    /* =====================================================
       GRID LINES
    ===================================================== */

    let gridLines = "";

    const gridCount = 5;


    for (
        let i = 0;
        i <= gridCount;
        i++
    ) {

        const value =
            minValue +
            (
                (
                    maxValue -
                    minValue
                ) *
                (
                    i /
                    gridCount
                )
            );


        const y =
            yPosition(value);


        gridLines += `

            <line
                x1="${paddingLeft}"
                y1="${y}"
                x2="${width - paddingRight}"
                y2="${y}"
                stroke="#dbe3ef"
                stroke-width="1"
            />

            <text
                x="${paddingLeft - 12}"
                y="${y + 5}"
                text-anchor="end"
                font-size="13"
                fill="#64748b"
            >
                ${formatCurrency(value)}
            </text>

        `;
    }


    /* =====================================================
       CURRENT MARKER
    ===================================================== */

    const currentMarker = `

        <line
            x1="${currentX}"
            y1="${paddingTop}"
            x2="${currentX}"
            y2="${height - paddingBottom}"
            stroke="#ef4444"
            stroke-width="2"
            stroke-dasharray="6 6"
        />

        <circle
            cx="${currentX}"
            cy="${currentY}"
            r="8"
            fill="#ef4444"
        />

        <text
            x="${currentX}"
            y="${currentY - 18}"
            text-anchor="middle"
            font-size="14"
            font-weight="700"
            fill="#dc2626"
        >
            Your Bike
        </text>

    `;


    /* =====================================================
       X LABELS
    ===================================================== */

    let xLabels = "";


    for (
        let age = 0;
        age <= maxAge;
        age += 12
    ) {

        const x =
            xPosition(age);


        xLabels += `

            <text
                x="${x}"
                y="${height - 35}"
                text-anchor="middle"
                font-size="13"
                fill="#64748b"
            >
                ${age} mo
            </text>

        `;
    }


    /* =====================================================
       RENDER CHART
    ===================================================== */

    depreciationChart.innerHTML = `

        <div class="personalized-chart">

            <div class="chart-summary">

                <div>

                    <span>
                        Original Price
                    </span>

                    <strong>
                        ${formatCurrency(
                            launchPrice
                        )}
                    </strong>

                </div>


                <div>

                    <span>
                        Current Value
                    </span>

                    <strong>
                        ${formatCurrency(
                            predictedPrice
                        )}
                    </strong>

                </div>


                <div>

                    <span>
                        Bike Age
                    </span>

                    <strong>
                        ${currentAge} months
                    </strong>

                </div>

            </div>


            <svg
                viewBox="0 0 ${width} ${height}"
                width="100%"
                height="420"
                role="img"
                aria-label="Personalized bike depreciation chart"
            >

                ${gridLines}


                <polygon
                    points="${areaPoints}"
                    fill="rgba(37, 99, 235, 0.10)"
                />


                <polyline
                    points="${linePoints}"
                    fill="none"
                    stroke="#2563eb"
                    stroke-width="5"
                    stroke-linecap="round"
                    stroke-linejoin="round"
                />


                <line
                    x1="${paddingLeft}"
                    y1="${height - paddingBottom}"
                    x2="${width - paddingRight}"
                    y2="${height - paddingBottom}"
                    stroke="#94a3b8"
                    stroke-width="2"
                />


                ${currentMarker}


                ${xLabels}


                <text
                    x="${width / 2}"
                    y="${height - 5}"
                    text-anchor="middle"
                    font-size="14"
                    font-weight="600"
                    fill="#334155"
                >
                    Bike Age
                </text>

            </svg>


            <div class="chart-note">

                📉 The chart is personalized using your
                original price, current bike age and
                predicted resale value.

            </div>

        </div>

    `;
}


/* =========================================================
   DISPLAY SUCCESS RESULT
========================================================= */

function showResult(data) {

    const price =
        Number(
            data.estimated_resale_price
        );


    if (
        !Number.isFinite(price)
    ) {

        showError(
            "The server returned an invalid prediction."
        );

        return;
    }


    const brand =
        data.brand ||
        brandSelect.value;


    const model =
        data.model ||
        modelSelect.value;


    /*
     * Display prediction FIRST.
     *
     * Image is loaded separately afterwards.
     */

    result.innerHTML = `

        <div class="result-icon">
            💰
        </div>


        <div class="prediction-label">
            Estimated Market Resale Price
        </div>


        <div class="prediction-price">
            ${formatCurrency(price)}
        </div>


        <div class="prediction-label">
            ${brand} ${model}
        </div>


        <div class="result-details">

            <div>

                <span>
                    Depreciation
                </span>

                <strong>
                    ${formatCurrency(
                        data.depreciation_amount
                    )}
                </strong>

            </div>


            <div>

                <span>
                    Depreciation Rate
                </span>

                <strong>
                    ${Number(
                        data.depreciation_percentage
                    ).toFixed(2)}%
                </strong>

            </div>


            <div>

                <span>
                    Value Retained
                </span>

                <strong>
                    ${Number(
                        data.value_retained_percentage
                    ).toFixed(2)}%
                </strong>

            </div>

        </div>

    `;


    /*
     * NOW load the actual bike image.
     *
     * This happens only after successful prediction.
     */

    loadBikeImageAfterPrediction(
        brand,
        model
    );


    /*
     * Scroll to result.
     */

    if (resultSection) {

        resultSection.scrollIntoView({
            behavior: "smooth",
            block: "center"
        });

    }
}


/* =========================================================
   COLLECT FORM DATA
========================================================= */

function getFormData() {

    return {

        brand:
            brandSelect.value,

        model:
            modelSelect.value.trim(),

        engineCC:
            engineSelect.value,

        ageMonths:
            ageInput.value,

        kmDriven:
            kmInput.value,

        owners:
            ownersSelect.value,

        condition:
            conditionSelect.value,

        launchPrice:
            launchPriceInput.value

    };
}


/* =========================================================
   VALIDATE FORM
========================================================= */

function validateForm(data) {

    if (
        !data.brand ||
        !data.model ||
        !data.engineCC ||
        !data.ageMonths ||
        !data.kmDriven ||
        !data.owners ||
        !data.condition ||
        !data.launchPrice
    ) {

        return "Please fill in all bike details.";
    }


    const engineCC =
        Number(data.engineCC);


    const ageMonths =
        Number(data.ageMonths);


    const kmDriven =
        Number(data.kmDriven);


    const owners =
        Number(data.owners);


    const launchPrice =
        Number(data.launchPrice);


    if (
        !Number.isFinite(engineCC) ||
        engineCC <= 0
    ) {

        return "Engine capacity must be greater than 0.";
    }


    if (
        !Number.isFinite(ageMonths) ||
        ageMonths < 1
    ) {

        return "Bike age must be at least 1 month.";
    }


    if (
        ageMonths > 180
    ) {

        return "Bike age cannot exceed 180 months.";
    }


    if (
        !Number.isFinite(kmDriven) ||
        kmDriven < 0
    ) {

        return "Kilometers driven cannot be negative.";
    }


    if (
        kmDriven > 500000
    ) {

        return "Kilometers driven cannot exceed 500,000.";
    }


    if (
        !Number.isFinite(owners) ||
        owners < 1
    ) {

        return "Number of owners must be at least 1.";
    }


    if (
        !Number.isFinite(launchPrice) ||
        launchPrice <= 0
    ) {

        return "Launch price must be greater than 0.";
    }


    return null;
}


/* =========================================================
   SHOW LOADING
========================================================= */

function showPredictionLoading() {

    predictButton.disabled = true;


    predictButton.innerHTML = `
        ⏳ Calculating Resale Value...
    `;


    /*
     * IMPORTANT:
     *
     * Hide previous bike image while calculating.
     */

    hideBikeImage();


    result.innerHTML = `

        <div class="result-icon">
            🤖
        </div>


        <div
            class="prediction-price"
            style="font-size: 24px;"
        >
            Calculating...
        </div>


        <p>
            Our machine learning model is
            calculating the estimated resale value.
        </p>

    `;
}


/* =========================================================
   RESTORE BUTTON
========================================================= */

function restorePredictionButton() {

    predictButton.disabled = false;


    predictButton.innerHTML = `

        <span>
            ANALYZE MARKET VALUE
        </span>

        <i data-lucide="arrow-right"></i>

    `;


    /*
     * Re-create Lucide icon after replacing
     * button HTML.
     */

    if (
        typeof lucide !== "undefined"
    ) {

        lucide.createIcons();
    }
}


/* =========================================================
   SUBMIT PREDICTION
========================================================= */

if (predictionForm) {

    predictionForm.addEventListener(
        "submit",
        async function (event) {

            event.preventDefault();


            /*
             * Collect form data.
             */

            const formData =
                getFormData();


            /*
             * Validate.
             */

            const validationError =
                validateForm(
                    formData
                );


            if (validationError) {

                showError(
                    validationError
                );

                return;
            }


            /*
             * Start loading.
             */

            showPredictionLoading();


            try {

                const params =
                    new URLSearchParams({

                        brand:
                            formData.brand,

                        model_name:
                            formData.model,

                        engine_cc:
                            formData.engineCC,

                        age_months:
                            formData.ageMonths,

                        km_driven:
                            formData.kmDriven,

                        owners:
                            formData.owners,

                        condition:
                            formData.condition,

                        launch_price:
                            formData.launchPrice

                    });


                /*
                 * ======================================
                 * PREDICTION REQUEST
                 * ======================================
                 *
                 * Your original API endpoint is preserved.
                 */

                const response =
                    await fetch(
                        `${API_URL}/predict?${params.toString()}`
                    );


                if (!response.ok) {

                    const message =
                        await getApiError(
                            response,
                            "Unable to get prediction from the server."
                        );


                    throw new Error(
                        message
                    );
                }


                /*
                 * Read response.
                 */

                const data =
                    await response.json();


                /*
                 * Validate prediction.
                 */

                if (
                    data.estimated_resale_price === undefined ||
                    data.estimated_resale_price === null
                ) {

                    throw new Error(
                        "The server returned an invalid prediction."
                    );
                }


                /*
                 * ======================================
                 * DISPLAY RESULT
                 * ======================================
                 */

                showResult(
                    data
                );


                /*
                 * ======================================
                 * CREATE CHART
                 * ======================================
                 */

                createDepreciationChart(

                    Number(
                        formData.launchPrice
                    ),

                    Number(
                        formData.ageMonths
                    ),

                    Number(
                        data.estimated_resale_price
                    )

                );


            } catch (error) {

                console.error(
                    "Prediction error:",
                    error
                );


                showError(

                    error.message ||

                    "Could not connect to the prediction server."

                );


            } finally {

                restorePredictionButton();

            }

        }
    );
}


/* =========================================================
   BACKEND HEALTH CHECK
========================================================= */

async function checkBackend() {

    try {

        const response =
            await fetch(
                `${API_URL}/health`
            );


        if (!response.ok) {

            console.warn(
                "Backend is running but health check failed."
            );

            return;
        }


        const data =
            await response.json();


        console.log(
            "Bike Resale Prediction API connected successfully."
        );


        if (
            data.bike_variants !== undefined
        ) {

            console.log(
                `Available bike variants: ${data.bike_variants}`
            );

        }


    } catch (error) {

        console.warn(
            "Backend is not currently available."
        );

    }
}


/* =========================================================
   INITIALIZE
========================================================= */

document.addEventListener(
    "DOMContentLoaded",
    function () {

        /*
         * VERY IMPORTANT:
         *
         * Page starts with NO bike image.
         */

        hideBikeImage();


        /*
         * Check backend.
         */

        checkBackend();

    }
);