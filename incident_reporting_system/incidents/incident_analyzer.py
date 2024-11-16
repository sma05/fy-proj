from transformers import pipeline

class IncidentAnalyzer:
    def __init__(self):
        # Load the Hugging Face model for text generation
        self.summarizer = pipeline("summarization", model="facebook/bart-large-cnn")  # Example model

    def analyze_incident(self, title: str, description: str, incident_type: str) -> dict:
        """
        Analyze and enhance the incident title and description using a Hugging Face model.
        
        Args:
            title: The title of the incident
            description: The description of the incident
            incident_type: The type of incident
            
        Returns:
            A dictionary containing the enhanced summary
        """
        # Combine title and description for analysis
        combined_text = f"Title: {title}\nDescription: {description}\nIncident Type: {incident_type}"
        
        # Generate a summary of the combined text
        summary = self.summarizer(combined_text, max_length=150, min_length=30, do_sample=False)
        
        return {
            'summary': summary[0]['summary_text'],  # Enhanced summary
        }