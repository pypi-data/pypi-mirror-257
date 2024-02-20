from apify_client import ApifyClient

class InstaScraper:
    def __init__(self):
        """
        Initialize the InstaScraper with default API key and actor ID.
        """
        self.api_key = "apify_api_BXEYPBO2DM54wlpErd0ibwBC7Zavzj2DfCvS"
        self.actor_id = "dSCLg0C3YEZ83HzYX"
        self.client = ApifyClient(self.api_key)

    def Scraper(self, input_data):
        """
        Run an Apify actor with the default actor ID and the provided input data.

        Parameters:
            input_data (dict): The input data for the actor.

        Returns:
            list: A list of items fetched from the actor's run dataset.
        """
        # Call the Apify actor with the provided input data
        run = self.client.actor(self.actor_id).call(run_input=input_data)

        # Fetch and print Actor results from the run's dataset (if there are any)
        results = []
        for item in self.client.dataset(run["defaultDatasetId"]).iterate_items():
            results.append(item)
        
        return results
