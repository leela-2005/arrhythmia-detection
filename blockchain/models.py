from django.db import models

class BlockchainRecord(models.Model):
    record_id = models.CharField(max_length=100)
    predicted_class = models.CharField(max_length=50)
    confidence_score = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)
    shap_summary = models.TextField()
    
    # Store the generated SHA-256 Hash
    stored_hash = models.CharField(max_length=256)
    
    # Store Tx Receipt hash from the local web3 simulated blockchain
    transaction_receipt = models.CharField(max_length=256, null=True, blank=True)

    def __str__(self):
        return f"{self.record_id} - {self.stored_hash[:15]}..."
