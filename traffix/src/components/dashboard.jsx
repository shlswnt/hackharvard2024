// components/Dashboard.jsx
import { Card } from "@/components/ui/card";
import { Table, TableHeader, TableRow, TableCell } from "@/components/ui/table";
import { LineChart, Line, XAxis, YAxis, Tooltip, CartesianGrid, ResponsiveContainer } from 'recharts';
import { useEffect } from "react";

export default function Dashboard({ roadData, children }) {
  // Log the full roadData to check what is available
  useEffect(() => {
    console.log("Road Data:", roadData.name);
  }, [roadData]);

  // Construct the video URL using the road name
  const videoUrl = roadData ? `http://localhost:8000/video/?name=${roadData.name}` : "";

  // Log the video URL only when it exists
  useEffect(() => {
    if (videoUrl) {
      console.log("Video URL:", videoUrl);
    } else {
      console.log("No video URL available");
    }
  }, [videoUrl]);

  // Return early if no road data is available
  if (!roadData) {
    return <p>No data available for this road.</p>;
  }

  const weatherPenalties = roadData.weather_penalties;

  // Prepare line chart data
  const chartData = [
    { name: 'Rain', value: weatherPenalties.rain[1] },
    { name: 'Snow', value: weatherPenalties.snow[1] },
    { name: 'Freezing Rain', value: weatherPenalties.freezing_rain[1] },
    { name: 'Cold Temp', value: weatherPenalties.cold_temp[1] },
    { name: 'Hot Temp', value: weatherPenalties.hot_temp[1] },
  ];

  return (
    <div className="p-4 space-y-4">
      <div className="flex space-x-4">
        {/* Video Feed */}
        <Card className="flex-grow p-4 w-1/2">
          <h2 className="text-lg font-bold mb-4">Live Video Feed</h2>
          <div className="flex justify-center">
            {children}
          </div>
        </Card>

        {/* Road Information */}
        <Card className="flex-grow p-4 w-1/2">
          <h2 className="text-lg font-bold mb-4">Road Information</h2>
          <Table>
            <TableHeader>
              <TableRow>
                <TableCell>Attribute</TableCell>
                <TableCell>Value</TableCell>
              </TableRow>
            </TableHeader>
            <tbody>
              <TableRow>
                <TableCell>City</TableCell>
                <TableCell>{roadData.city}</TableCell>
              </TableRow>
              <TableRow>
                <TableCell>Latitude</TableCell>
                <TableCell>{roadData.latitude}</TableCell>
              </TableRow>
              <TableRow>
                <TableCell>Longitude</TableCell>
                <TableCell>{roadData.longitude}</TableCell>
              </TableRow>
              <TableRow>
                <TableCell>Last Maintenance Date</TableCell>
                <TableCell>{roadData.last_maintenance_date}</TableCell>
              </TableRow>
              <TableRow>
                <TableCell>Vehicle Score</TableCell>
                <TableCell>{roadData.vehicle_score_last_maintenance}</TableCell>
              </TableRow>
              <TableRow>
                <TableCell>Weather Score</TableCell>
                <TableCell>{roadData.weather_score_last_maintenance}</TableCell>
              </TableRow>
            </tbody>
          </Table>
        </Card>
      </div>

      {/* Weather Penalties Line Chart */}
      <Card className="p-4">
        <h2 className="text-lg font-bold mb-4">Weather Penalties Chart</h2>
        <ResponsiveContainer width="100%" height={300}>
          <LineChart data={chartData}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey="name" />
            <YAxis />
            <Tooltip />
            <Line type="monotone" dataKey="value" stroke="#8884d8" activeDot={{ r: 8 }} />
          </LineChart>
        </ResponsiveContainer>
      </Card>
    </div>
  );
}