const paragraphInput = document.getElementById("paragraph");
const extractBtn = document.getElementById("extractBtn");
const results = document.getElementById("results");
const errorBox = document.getElementById("error");

const fields = [
    "Movie Name",
    "Genre",
    "Cast",
    "Director",
    "Release Year",
    "Main Characters",
    "Plot",
    "Themes",
    "Setting",
    "Important Keywords",
    "Quick Summary"
];

function parseExtraction(text) {
    const data = {};

    fields.forEach((field, index) => {
        const nextField = fields[index + 1];

        const currentEscaped = field.replace(
            /[.*+?^${}()|[\]\\]/g,
            "\\$&"
        );

        let regex;

        if (nextField) {
            const nextEscaped = nextField.replace(
                /[.*+?^${}()|[\]\\]/g,
                "\\$&"
            );

            regex = new RegExp(
                "^" +
                currentEscaped +
                "\\s*:\\s*([\\s\\S]*?)(?=\\n" +
                nextEscaped +
                "\\s*:)",
                "im"
            );
        } else {
            regex = new RegExp(
                "^" +
                currentEscaped +
                "\\s*:\\s*([\\s\\S]*)$",
                "im"
            );
        }

        const match = text.match(regex);

        data[field] =
            match && match[1].trim()
                ? match[1].trim()
                : "Not mentioned";
    });

    return data;
}

function renderResults(data) {
    results.innerHTML = "";

    fields.forEach(fieldName => {
        const field = document.createElement("div");
        field.className = "field";

        const name = document.createElement("div");
        name.className = "field-name";
        name.textContent = fieldName;

        const value = document.createElement("div");
        value.className = "field-value";
        value.textContent = data[fieldName] || "Not mentioned";

        field.appendChild(name);
        field.appendChild(value);

        results.appendChild(field);
    });
}

async function extractInformation() {
    const paragraph = paragraphInput.value.trim();

    errorBox.textContent = "";

    if (!paragraph) {
        errorBox.textContent = "Enter a movie paragraph.";
        return;
    }

    extractBtn.classList.add("loading");
    extractBtn.disabled = true;

    try {
        const response = await fetch("/extract", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                paragraph: paragraph
            })
        });

        const data = await response.json().catch(() => null);

        if (!response.ok) {
            const errDetail = data && (data.error || data.detail || data.message);
            throw new Error(errDetail || `Server error (${response.status})`);
        }

        const extractedText =
            (data && (data.result || data.content)) || "";

        if (!extractedText) {
            throw new Error("No extraction result was returned.");
        }

        const extractedData = parseExtraction(extractedText);

        renderResults(extractedData);

    } catch (error) {
        console.error(error);

        errorBox.textContent =
            error.message ||
            "Unable to connect to the extraction backend.";

    } finally {
        extractBtn.classList.remove("loading");
        extractBtn.disabled = false;
    }
}

const sample1Text = `Inception is a 2010 science fiction action film written and directed by Christopher Nolan. The film stars Leonardo DiCaprio as Dom Cobb, a professional thief who steals corporate secrets by infiltrating the subconscious minds of his targets. The cast also features Joseph Gordon-Levitt as Arthur, Elliot Page as Ariadne, and Tom Hardy as Eames. Set in various surreal dream worlds and modern metropolitan cities, the plot revolves around a dangerous final mission called inception—planting an idea into a CEO's mind rather than stealing it. Major themes include reality versus illusion, grief, guilt, and the subconscious mind.`;

const sample2Text = `The Dark Knight is a 2008 superhero action movie directed by Christopher Nolan. It stars Christian Bale as billionaire Bruce Wayne, also known as the vigilante Batman, who protects Gotham City from criminal syndicates. The film stars Heath Ledger as the psychopathic criminal mastermind known as the Joker, alongside Gary Oldman as Lieutenant James Gordon and Aaron Eckhart as District Attorney Harvey Dent. Set against the dark and gritty backdrop of Gotham City, the story chronicles Batman's psychological and physical struggle to stop the Joker from plunging the city into complete anarchy. Central themes explore justice, chaos, moral corruption, heroism, and personal sacrifice.`;

const sample1Btn = document.getElementById("sample1Btn");
const sample2Btn = document.getElementById("sample2Btn");

if (sample1Btn) {
    sample1Btn.addEventListener("click", () => {
        paragraphInput.value = sample1Text;
        paragraphInput.focus();
    });
}

if (sample2Btn) {
    sample2Btn.addEventListener("click", () => {
        paragraphInput.value = sample2Text;
        paragraphInput.focus();
    });
}

extractBtn.addEventListener("click", extractInformation);

paragraphInput.addEventListener("keydown", function (event) {
    if (event.ctrlKey && event.key === "Enter") {
        extractInformation();
    }
});