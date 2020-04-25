function getDistance(lat1, long1, lat2, long2) {
                var R = 3959; // miles
                var dLat = (lat1-(lat2))*(Math.PI/180);
                var dLon = -(long1-(long2))*(Math.PI/180);
                var rlat1 = lat1*(Math.PI/180);
                var rlat2 = lat2*(Math.PI/180);
                var a = Math.sin(dLat/2) * Math.sin(dLat/2) + Math.sin(dLon/2) * Math.sin(dLon/2) * Math.cos(rlat1) * Math.cos(rlat2); 
                var c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1-a));
                var d = R * c;
                return d;
		    }
