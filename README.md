# Survaize

<div align="center">
<svg width="300" height="240" viewBox="0 0 300 240" xmlns="http://www.w3.org/2000/svg" aria-hidden="true">

  <defs>
    <!-- Gradients for the logo emblem -->
    <radialGradient id="cloudGradient" cx="0.3" cy="0.3" r="0.8">
      <stop offset="0%" style="stop-color:#90EE90;stop-opacity:1" />
      <stop offset="100%" style="stop-color:#32CD32;stop-opacity:1" />
    </radialGradient>
    
    <linearGradient id="handleGradient" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" style="stop-color:#FF4444;stop-opacity:1" />
      <stop offset="50%" style="stop-color:#CC0000;stop-opacity:1" />
      <stop offset="100%" style="stop-color:#AA0000;stop-opacity:1" />
    </linearGradient>
    
    <linearGradient id="ferruleGradient" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" style="stop-color:#E0E0E0;stop-opacity:1" />
      <stop offset="50%" style="stop-color:#C0C0C0;stop-opacity:1" />
      <stop offset="100%" style="stop-color:#A0A0A0;stop-opacity:1" />
    </linearGradient>
  </defs>

  <!-- Robot group -->
  <g id="robotBounce">
    <animateTransform attributeName="transform"
      type="translate"
      values="120,50;120,40;120,50" 
      keyTimes="0;0.5;1"
      dur="4s"
      repeatCount="indefinite"
    />

    <!-- Legs -->
    <rect x="10" y="100" width="12" height="25" rx="4" fill="#2f66f3" />
    <rect x="38" y="100" width="12" height="25" rx="4" fill="#2f66f3" />

    <!-- Feet (bouncing along with the body) -->
    <ellipse cx="16" cy="126" rx="8" ry="4" fill="#444" />
    <ellipse cx="44" cy="126" rx="8" ry="4" fill="#444" />

    <!-- Arms -->
    <line x1="-10" y1="80" x2="5" y2="70" stroke="#2f66f3" stroke-width="6" stroke-linecap="round" />
    <line x1="70" y1="80" x2="55" y2="70" stroke="#2f66f3" stroke-width="6" stroke-linecap="round" />
    <circle cx="-10" cy="80" r="6" fill="#2f66f3" />
    <circle cx="70" cy="80" r="6" fill="#2f66f3" />

    <!-- Torso -->
    <rect x="5" y="60" width="50" height="40" rx="10" fill="#2f66f3" />

    <!-- Logo emblem on chest -->
    <g id="logoEmblem" transform="translate(10, 65) scale(0.09)">
      <!-- Cloud shape -->
      <path d="M 80 140 
               C 60 140, 45 125, 45 105
               C 45 85, 60 70, 80 70
               C 85 50, 105 35, 130 35
               C 155 35, 175 50, 180 70
               C 200 70, 215 85, 215 105
               C 215 125, 200 140, 180 140
               L 80 140
               Z" 
            fill="url(#cloudGradient)" 
            stroke="#228B22" 
            stroke-width="2"/>
      
      <!-- Cloud highlight/shine -->
      <ellipse cx="110" cy="85" rx="25" ry="15" fill="#B8FFB8" opacity="0.6"/>
      
      <!-- Swirl pattern on cloud -->
      <path d="M 90 110 
               C 110 105, 120 115, 115 125
               C 110 135, 95 130, 100 120
               C 105 115, 110 118, 108 120" 
            fill="none" 
            stroke="#66BB6A" 
            stroke-width="2" 
            stroke-linecap="round"/>
      
      <!-- Paintbrush handle -->
      <rect x="120" y="10" width="8" height="80" 
            fill="url(#handleGradient)" 
            stroke="#990000" 
            stroke-width="1"
            transform="rotate(45 124 85)"/>
        
      <!-- Brush bristles -->
      <ellipse cx="77" cy="133" rx="4" ry="12" 
               fill="#4A4A4A" 
               transform="rotate(45 124 152)"/>
      
      <!-- Brush tip -->
      <ellipse cx="71.5" cy="141" rx="2" ry="6" 
               fill="#2A2A2A" 
               transform="rotate(45 124 160)"/>

      <!-- Brush ferrule (metal band) -->
      <rect x="86.5" y="105" width="8" height="15" 
            fill="url(#ferruleGradient)" 
            stroke="#888888" 
            stroke-width="1"
            transform="rotate(45 124 132.5)"/>

      <!-- Handle highlight -->
      <rect x="121" y="12" width="2" height="76" 
            fill="#FF8888" 
            opacity="0.7"
            transform="rotate(45 122 85)"/>
    </g>

    <!-- Neck -->
    <rect x="25" y="50" width="10" height="10" fill="#2f66f3" />

    <!-- Head -->
    <rect x="0" y="0" rx="12" ry="12" width="60" height="50" fill="#2f66f3" />
    <rect x="10" y="10" width="40" height="30" rx="8" ry="8" fill="#8ecaff" />

    <!-- Eyes -->
    <circle cx="20" cy="25" r="5" fill="#fff" />
    <circle cx="20" cy="25" r="2" fill="#333">
      <animate attributeName="cx" values="19;21;19" dur="1.5s" repeatCount="indefinite" />
    </circle>
    <circle cx="40" cy="25" r="5" fill="#fff" />
    <circle cx="40" cy="25" r="2" fill="#333">
      <animate attributeName="cx" values="39;41;39" dur="1.5s" repeatCount="indefinite" />
    </circle>

    <!-- Smile & Eyebrows -->
    <path d="M22 35 Q30 42 38 35" stroke="#333" stroke-width="2" fill="none" />
    <line x1="15" y1="18" x2="25" y2="16" stroke="#333" stroke-width="2" stroke-linecap="round" />
    <line x1="35" y1="16" x2="45" y2="18" stroke="#333" stroke-width="2" stroke-linecap="round" />

    <!-- Antenna -->
    <line x1="30" y1="-15" x2="30" y2="0" stroke="#333" stroke-width="4" />
    <circle cx="30" cy="-15" r="5" fill="#333" />
  </g>

  <!-- Paper (moving with lines) -->
  <g id="paper">
      <animateTransform attributeName="transform"
        type="translate"
        values="0 0; 65 -40; 65 -40; 170 0"
        keyTimes="0; 0.3; 0.6; 1"
        dur="4s"
        repeatCount="indefinite"
      />
    <rect x="47" y="130" width="26" height="34" rx="2" ry="2" fill="#fff" stroke="#ccc">
    </rect>

    <!-- Simulated text lines -->
    <g stroke="#8ecaff" stroke-width="1">
      <line x1="49" y1="135" x2="70" y2="135">
      </line>
      <line x1="49" y1="140" x2="70" y2="140">
      </line>
      <line x1="49" y1="145" x2="70" y2="145">
      </line>
    </g>
  </g>

</svg>
</div>

Survaize is a tool that automatically converts "paper" questionnaires into interactive survey apps. It uses a combination of OCR and generative AI vision models to understand the structure of survey questionnaires in order to generate survey apps compatible with data collection platforms like [CSPro](https://www.census.gov/data/software/cspro.html).

## Features

- Read PDF questionnaires 
- Intelligent survey structure recognition using Generative AI
- Conversion to intermediate JSON format
- Export to popular survey platforms (CSPro, others in the future)

## Installation

Eventually this will be published to PyPI but for now follow the instructions in [installation.md](installation.md).

## Setup
Survaize requires an OpenAI API key. You can specify it using the --api-key parameter or by setting in the OPENAI_API_KEY environment variable.

If you do not already have an account on the [OpenAI developer platform](https://platform.openai.com/docs/overview) you will need to sign up to get a key.

Survaize should also work with other LLM providers that have OpenAI compatible APIs by providing the appropriate API URL and model name via the --api-url and --api-model arguments or the OPENAI_API_URL and OPENAI_MODEL environment variables. Note that only LLMs that support vision will work.

To use Azure OpenAI you will need to specify the key, URL, API version and deployment name. For example:

```
OPENAI_API_KEY="XXXXXXXXXXXXXXXXXXXXXXXX"
OPENAI_API_VERSION="2025-04-01-preview"
OPENAI_API_URL="https://myazuredeploy-openai.openai.azure.com/"
OPENAI_API_DEPLOYMENT="my-gpt-4.1-deployment"
```

Alternatively, you can pass those variables as command line arguments to survaize (run `survaize --help` for details).

## Running

## Interactive Mode
To run Survaize in interactive mode, execute the `ui` command:

```shell
survaize ui
```

This will start a local web server and open the Survaize UI in your default web browser. You can then upload a questionnaire,
and Survaize will read it, analyze its structure, and display the results in the browser. From there you can then export the questionnaire to
CSPro or other formats.

## Non-Interactive Mode
To convert a PDF questionnaire to CSPro using the command line interface (non-interactive mode), you can use the `convert` 
command. The basic syntax is:

```shell
survaize convert input_file output_file --format cspro
```

For example:

```shell
survaize convert examples/PopstanHouseholdQuestionnaire.pdf output/PopstanHouseholdSurvey --format cspro
```
will generate a complete CSPro application (dictionary, forms...) in the directory `output/PopstanHouseholdSurvey`.

Survaize uses JSON as an intermediate format so JSON files can be used as input or output files. The above command could be split into two using an intermediate JSON file:

```shell
survaize convert examples/PopstanHouseholdQuestionnaire.pdf output/PopstanHouseholdSurvey.json --format json
survaize convert output/PopstanHouseholdSurvey.json output/PopstanHouseholdSurvey --format cspro
```

You can even hand edit the intermediate JSON file before generating the CSPro application.

## Development

This project uses Python and UV as the package manager. To install see [installation.md](installation.md).

For development workflows, see [development.md](development.md).

For instructions on publishing to PyPI, see [publishing.md](publishing.md).

## License

MIT 

## TODO
- Correctly handle location question type (produce two fields in CSPro)
- Fills in CAPI question text
- Evals (in progress)
- Questionnaire edits in the UI