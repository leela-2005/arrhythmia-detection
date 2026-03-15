from django.shortcuts import render
from blockchain.quantum_chain import blockchain

def blockchain_view(request):
    return render(request, "blockchain/ledger.html", {
        "blocks": reversed(blockchain)
    })
