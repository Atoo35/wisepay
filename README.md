# WisePay

WisePay is a Python-based application that integrates Splitwise and Payman services to provide a seamless payment experience. It allows users to manage their Splitwise expenses and make payments through Payman's payment platform.

## Features

- Splitwise Integration

  - OAuth2 authentication
  - Group management
  - Debt tracking
  - User information retrieval

- Payman Integration

  - Balance checking
  - Payee management
  - Payment processing
  - Support for multiple payment types (Wallet, Crypto, ACH)

- AI-Powered Chat Interface
  - Natural language processing for expense management
  - Automated debt settlement
  - Smart payee creation and management

## Project Structure

```
.
├── app/
│   ├── config.py         # Configuration settings
│   ├── server.py         # FastAPI server and endpoints
│   ├── tools.py          # Core functionality and API integrations
│   ├── services/         # Service layer implementations
│   ├── models/          # Data models and schemas
│   └── db/              # Database operations
├── .env                 # Environment variables
├── chat_ui.py          # Chat interface implementation
├── index.html          # Frontend interface
└── run.py              # Application entry point
```

## Prerequisites

- Python 3.x
- Virtual environment
- Splitwise API credentials
- Payman API credentials

## Setup

1. Clone the repository:

```bash
git clone <repository-url>
cd wisepay
```

2. Create and activate a virtual environment:

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Configure environment variables:
   Create a `.env` file with the following variables:

```
SPLITWISE_API_KEY=your_splitwise_api_key
SPLITWISE_API_SECRET=your_splitwise_api_secret
REDIRECT_URI=your_redirect_uri
```

## Initial Setup and Authentication

1. Start the FastAPI server:

```bash
python run.py
```

2. Visit `http://localhost:8000/init-auth` to begin the OAuth2 flow with Splitwise
3. Complete the authentication process
4. The OAuth token will be stored in the database for future use
5. Close the terminal and run the `chat_ui.py` file

## Using the Chat Interface

After the initial setup, you can use the Gradio chat interface for all operations. The AI will automatically use your stored OAuth token from the database.

### Example Prompts

1. **View Groups and Debts**

   ```
   "Show me all the groups I belong to and my current debts in each group"
   ```

2. **Check and Create Payman Payees**

   ```
   "Check if the people I owe money to exist on Payman. If not, create them as payees"
   ```

3. **Settle Specific Debt**

   ```
   "I want to settle my debt with John Doe in the 'Vacation' group"
   ```

4. **Check Payman Balance**

   ```
   "What's my current Payman balance?"
   ```

5. **Create Payee and Settle Debt**

   ```
   "Create a Payman payee for Sarah Smith and settle my $50 debt with her"
   ```

6. **View All Debts**

   ```
   "Show me all my current debts across all groups"
   ```

7. **Settle Multiple Debts**
   ```
   "Settle all my debts in the 'Roommates' group"
   ```

## Workflow

1. **Initial Setup**

   - Start FastAPI server
   - Complete OAuth2 authentication
   - Store token in database

2. **Daily Usage**

   - Use Gradio chat interface
   - AI automatically retrieves your OAuth token
   - Perform operations through natural language

3. **Debt Settlement Process**
   - AI checks if payee exists on Payman
   - Creates payee if needed
   - Verifies user in database
   - Processes payment
   - Updates Splitwise status

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request
