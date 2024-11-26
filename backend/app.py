from flask import Flask, request, jsonify
from flask_cors import CORS
from dijkstra import ParkingRouter

app = Flask(__name__)
CORS(app)

# Initialize parking router
parking_router = ParkingRouter()

@app.route('/find_parking', methods=['POST'])
def find_parking():
    """
    API endpoint to find nearest parking slot
    """
    data = request.json
    
    # Validate input
    if not data or 'latitude' not in data or 'longitude' not in data:
        return jsonify({"error": "Invalid input. Latitude and longitude required."}), 400
    
    # Find nearest parking
    try:
        result = parking_router.find_nearest_parking(
            data['latitude'], 
            data['longitude']
        )
        
        if result:
            return jsonify({
                "parking_slot": result['slot'],
                "distance": result['distance']
            })
        else:
            return jsonify({"error": "No available parking found"}), 404
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)
