from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from datetime import datetime
from .serializers import CryptoDataSerializer
from .scraping import scrape_crypto_data

@api_view(['GET', 'POST'])
def get_crypto_data(request):
    if request.method == 'POST':
        date_str = request.data.get('date')
        if not date_str:
            return Response({"error": "Date is required"}, status=status.HTTP_400_BAD_REQUEST)

        # Convert the date string to the required format
        try:
            date = datetime.fromisoformat(date_str)
            formatted_date = date.strftime('%Y-%m-%d')
        except ValueError:
            return Response({"error": "Invalid date format"}, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'GET':
        # Use the current date
        formatted_date = datetime.now().strftime('%Y-%m-%d')

    try:
        coins_data = scrape_crypto_data(formatted_date)

    except Exception as e:
        # >>> NEW: print backend error for debugging <<<
        print(f"[ERROR] scrape_crypto_data failed for date {formatted_date}: {str(e)}")

        # >>> NEW: return clearer API error message <<<
        return Response(
            {"error": f"Failed to fetch crypto data: {str(e)}"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

    # >>> NEW: Validate API returned a list <<<
    if not isinstance(coins_data, list):
        print(f"[ERROR] Invalid data structure returned: {type(coins_data)}")
        return Response(
            {"error": "Scraper returned invalid data structure. Expected a list."},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

    # Filter out entries with null values
    filtered_coins_data = [
        coin for coin in coins_data
        if isinstance(coin, dict) and any(value is not None for value in coin.values())
    ]

    # >>> NEW: Debug print how many records survived filtering <<<
    print(f"[INFO] Received {len(coins_data)} coins, returning {len(filtered_coins_data)} after filtering.")

    # Serialize the data
    serializer = CryptoDataSerializer(filtered_coins_data, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)
