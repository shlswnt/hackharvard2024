"use client";

import { useState, useEffect } from 'react';
import { Card, CardHeader, CardTitle } from '@/components/ui/card';
import { cn } from '@/lib/utils'; // Import cn for conditional classes

export function RoadList({ searchTerm, selectedCity, onRoadSelect }) {
  const [roads, setRoads] = useState([]);
  const [loading, setLoading] = useState(true);
  const [selectedRoad, setSelectedRoad] = useState(null); // Track selected road

  const cityAliases = {
    "lv": "Las Vegas",
    "ny": "Manhattan",
    "at": "Atlanta"
  };

  useEffect(() => {
    async function fetchRoads() {
      try {
        const roadNamesResponse = await fetch("http://localhost:8000/get_all_names/");
        const roadNames = await roadNamesResponse.json();

        const roadDetailsPromises = roadNames.map(async (roadName) => {
          const response = await fetch(`http://localhost:8000/intersection/?name=${roadName}`);
          const roadDetails = await response.json();
          return {
            name: roadName,
            city: roadDetails.city,
          };
        });

        const allRoads = await Promise.all(roadDetailsPromises);
        setRoads(allRoads);
        setLoading(false);

        if (allRoads.length > 0 && !selectedRoad) {
          // Automatically select the first road if no road is selected
          const firstRoad = allRoads[0].name;
          setSelectedRoad(firstRoad);
          onRoadSelect(firstRoad); // Pass selected road to parent
        }
      } catch (error) {
        console.error("Error fetching road details:", error);
        setLoading(false);
      }
    }

    fetchRoads();
  }, [onRoadSelect, selectedRoad]);

  const handleCardClick = (roadName) => {
    setSelectedRoad(roadName); // Update selected road
    onRoadSelect(roadName); // Pass selected road to parent
  };

  const filteredRoads = roads.filter((road) => {
    const roadName = road.name ? road.name.toLowerCase() : "";
    const roadCity = cityAliases[road.city] || "";
    const matchesSearch = roadName.includes(searchTerm.toLowerCase());
    const matchesCity = selectedCity === "all" || roadCity === cityAliases[selectedCity];
    return matchesSearch && matchesCity;
  });

  return (
    <div className="h-[calc(100vh-4rem)] overflow-y-auto px-4 pt-4 space-y-4">
      {loading ? (
        <p>Loading roads...</p>
      ) : filteredRoads.length > 0 ? (
        filteredRoads.map((road) => (
          <Card
            key={road.name}
            className={cn(
              "p-4 cursor-pointer", 
              selectedRoad === road.name ? "bg-muted" : "bg-white" // Apply light gray background when selected
            )}
            onClick={() => handleCardClick(road.name)}
          >
            <CardHeader>
              <CardTitle>{road.name}</CardTitle>
            </CardHeader>
          </Card>
        ))
      ) : (
        <p>No roads found for the selected city or search term.</p>
      )}
    </div>
  );
}