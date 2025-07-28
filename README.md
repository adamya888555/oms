# Order Management System - Agentic Ai

## Installation

1. Clone the repository:
```
git clone https://github.com/your-username/OMS-Agentic-Ai.git
```
2. Navigate to the project directory:
```
cd dir
```
3. Install the required dependencies:
```
pip install -r requirements.txt
```

## Usage

1. Start the Streamlit application:
```
streamlit run main.py
```
2. The application will open in your default web browser.
3. Log in using the credentials.
4. You can now interact with the Order Management System by entering messages in the chat input field.

## API

The main components of the API are:

1. `OrderProcessor`: Handles the orchestration of LLM calls to process order queries and small talk.
2. `generate_order_status_summary`: Generates a detailed order status summary using the LLM.
3. `summarizer`: Creates a customer-friendly summary of the order status.

## Contributing

1. Fork the repository.
2. Create a new branch for your feature or bug fix.
3. Make your changes and commit them.
4. Push your changes to your forked repository.
5. Submit a pull request to the original repository.

## License

This project is licensed under the [MIT License](LICENSE).

## Testing

The project currently does not have any automated tests. However, you can manually test the application by interacting with it through the Streamlit interface.