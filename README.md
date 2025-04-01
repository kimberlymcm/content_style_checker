# Content Style Guide Checker

A web application that helps content writers ensure their text follows plain language guidelines and best practices. The application analyzes text input and provides real-time feedback on style issues, suggestions for improvement, and an automatically improved version of the text.

## Project Goals

The Content Style Guide Checker aims to:

1. **Improve Content Accessibility**
   - Make content easier to understand for all readers
   - Reduce cognitive load by simplifying complex language
   - Ensure consistent communication across platforms

2. **Streamline Content Creation**
   - Help writers identify common style issues in real-time
   - Provide immediate, actionable feedback
   - Automate the initial review process
   - Reduce the time spent on manual content reviews

3. **Maintain Style Guide Consistency**
   - Enforce plain language guidelines automatically
   - Encourage the use of active voice for clarity
   - Promote the use of simple terms over complex ones
   - Ensure abbreviations are properly defined
   - Make content more conversational through appropriate contractions

4. **Support Content Writers**
   - Provide a user-friendly interface for content checking
   - Offer clear explanations for each identified issue
   - Suggest specific improvements for problematic text
   - Generate improved versions of the text automatically

5. **Enhance Quality Assurance**
   - Reduce common writing errors before review
   - Ensure compliance with content standards
   - Create more consistent content across different writers
   - Facilitate the editorial review process

![Application Screenshot](docs/images/app-screenshot.png)

## Features

- **Real-time Analysis**: Instantly analyze text for common style guide violations
- **Color-coded Issue Highlighting**: 
  - 🔴 Red: Passive voice constructions
  - 🟠 Orange: Undefined abbreviations
  - 🟣 Purple: Complex words that can be simplified
  - 🔵 Blue: Phrases that should use contractions
- **Automatic Suggestions**: Provides specific recommendations for each issue
- **Improved Text Generation**: Automatically generates a corrected version of the text
- **Modern UI**: Built with React and Chakra UI for a clean, accessible interface

![Feature Demo](docs/images/feature-demo.gif)

## Technology Stack

- **Frontend**:
  - React 18.x with TypeScript 4.9.5
  - Chakra UI 2.7.1 for components
  - Axios for API requests
  - Node.js 14.15.0 or higher
  
- **Backend**:
  - FastAPI (Python 3.7+)
  - Pydantic for data validation
  - Uvicorn ASGI server
  - CORS middleware enabled

## Detailed Requirements

### System Requirements
- **Operating System**: 
  - macOS 10.15+
  - Windows 10+ 
  - Linux (Ubuntu 18.04+)
- **Memory**: 2GB RAM minimum
- **Disk Space**: 500MB free space
- **Browser**: 
  - Chrome 90+
  - Firefox 88+
  - Safari 14+
  - Edge 90+

### Development Requirements
- **Node.js**: v14.15.0 or higher
  ```bash
  node --version  # Check Node version
  ```
- **Python**: 3.7 or higher with pip
  ```bash
  python --version  # Check Python version
  pip --version     # Check pip version
  ```
- **Package Managers**:
  - npm 6.14.0+ or
  - yarn 1.22.0+

### Required Python Packages
```
fastapi==0.68.0
uvicorn==0.15.0
pydantic==1.8.2
```

### Required Node Packages
```json
{
  "@chakra-ui/react": "2.7.1",
  "@emotion/react": "11.11.1",
  "@emotion/styled": "11.11.0",
  "axios": "^1.3.4",
  "react": "^18.2.0",
  "react-dom": "^18.2.0",
  "typescript": "4.9.5"
}
```

## Installation

1. Clone the repository:
```bash
git clone [repository-url]
cd [repository-name]
```

2. Set up the backend:
```bash
cd backend
python -m venv venv  # Create virtual environment
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```
The backend server will start at http://localhost:8000

3. Set up the frontend:
```bash
cd frontend
npm install
npm start
```
The frontend development server will start at http://localhost:3000

## Usage

1. Open your browser and navigate to http://localhost:3000
2. Enter your text in the textarea
3. Click "Analyze Content"
4. Review the highlighted issues and suggestions
5. Use the improved text version if desired

### Example Input
```text
The form cannot be utilized until it has been completed by the applicant. The DMDC will implement new regulations that should not be ignored. The CIA and FBI agents will commence and terminate the investigation. The documents were being processed when the error occurred.
```

This sample text contains multiple style issues:
- Passive voice: "has been completed", "were being processed"
- Complex words: "utilized", "implement", "commence", "terminate"
- Undefined abbreviations: "DMDC", "CIA", "FBI"
- Phrases that could use contractions: "cannot", "will not", "should not"

### Expected Output
![Example Output](docs/images/example-output.png)

## Style Checks

The application currently checks for:

1. **Passive Voice**
   - Identifies common passive voice constructions
   - Suggests using active voice instead
   - Example: "has been completed" → "completed"

2. **Abbreviations**
   - Flags undefined abbreviations
   - Allows common abbreviations (e.g., US, FAQ)
   - Suggests defining abbreviations on first use
   - Example: "DMDC" → "Defense Manpower Data Center (DMDC)"

3. **Complex Words**
   - Identifies overly complex words
   - Suggests simpler alternatives
   - Examples:
     - "utilize" → "use"
     - "implement" → "start"
     - "facilitate" → "help"
     - "leverage" → "use"
     - "commence" → "begin"
     - "terminate" → "end"

4. **Contractions**
   - Identifies phrases that could use contractions
   - Makes content more conversational
   - Examples:
     - "cannot" → "can't"
     - "will not" → "won't"
     - "should not" → "shouldn't"
     - "do not" → "don't"

## Troubleshooting

### Common Issues and Solutions

1. **Backend Server Won't Start**
   - Error: "Address already in use"
     ```
     Solution: Kill the process using port 8000
     lsof -i :8000 | grep LISTEN
     kill -9 <PID>
     ```
   - Error: "Module not found"
     ```
     Solution: Ensure you're in the virtual environment
     source venv/bin/activate
     pip install -r requirements.txt
     ```

2. **Frontend Development Server Issues**
   - Error: "Module not found"
     ```
     Solution: Clear npm cache and reinstall
     npm cache clean --force
     rm -rf node_modules
     npm install
     ```
   - Error: "TypeScript errors"
     ```
     Solution: Check TypeScript version compatibility
     npm install typescript@4.9.5 --save-dev
     ```

3. **CORS Issues**
   - Error: "Access-Control-Allow-Origin missing"
     ```
     Solution: Ensure backend CORS middleware is properly configured
     Check main.py for correct CORS settings
     ```

4. **Node Version Issues**
   - Solution: Use nvm to install correct Node version
     ```bash
     curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.0/install.sh | bash
     source ~/.nvm/nvm.sh
     nvm install 14.15.0
     nvm use 14.15.0
     ```

### Performance Optimization

1. **Backend**
   - Use gunicorn for production deployment
   - Enable uvicorn workers
   ```bash
   gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker
   ```

2. **Frontend**
   - Create production build
   ```bash
   npm run build
   ```
   - Serve with nginx or similar

## Development

### Project Structure

```
.
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   └── main.py         # FastAPI application
│   ├── requirements.txt
│   └── venv/               # Python virtual environment
└── frontend/
    ├── src/
    │   ├── components/     # React components
    │   ├── types/         # TypeScript interfaces
    │   └── App.tsx        # Main application component
    ├── package.json
    └── tsconfig.json
```

### Adding New Style Checks

To add new style checks:

1. Add a new check function in `backend/app/main.py`
   ```python
   def check_new_style(text: str) -> List[ContentIssue]:
       # Implementation
       pass
   ```

2. Update the `analyze_content` endpoint to include the new check
   ```python
   issues.extend(check_new_style(text))
   ```

3. Add corresponding styling in the frontend's `getIssueColor` function
   ```typescript
   case 'new_style':
     return 'green';
   ```

4. Update this documentation

## Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch
   ```bash
   git checkout -b feature/amazing-feature
   ```
3. Commit your changes
   ```bash
   git commit -m 'Add amazing feature'
   ```
4. Push to the branch
   ```bash
   git push origin feature/amazing-feature
   ```
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Plain Language Guidelines and Best Practices
- FastAPI documentation
- React and Chakra UI communities 