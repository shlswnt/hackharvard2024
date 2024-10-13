"use client";

import { useState, useEffect } from "react";
import { Logo } from "@/components/logo";
import { SearchBar } from "@/components/search-bar";
import { MainNav } from "@/components/nav-main";
import { UserNav } from "@/components/nav-user";
import { ThemeToggle } from "@/components/theme-toggle";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { RoadList } from "@/components/road-list";
import Dashboard from "@/components/Dashboard"; // New Dashboard component

export default function Home() {
  const [searchTerm, setSearchTerm] = useState("");
  const [selectedCity, setSelectedCity] = useState("");
  const [selectedRoad, setSelectedRoad] = useState("");
  const [roadData, setRoadData] = useState(null); // Store road data

  const handleSearch = (term, city) => {
    setSearchTerm(term);
    setSelectedCity(city);
  };

  var videoUrl = "";

  const handleRoadSelect = async (road) => {
    setSelectedRoad(road);

    videoUrl = "http://localhost:8000/video/?name=" + road;
    console.log(videoUrl);

    // Fetch road data when a road is selected
    try {
      const response = await fetch(
        `http://localhost:8000/intersection/?name=${road}`
      );
      const data = await response.json();
      setRoadData(data); // Store road data
    } catch (error) {
      console.error("Error fetching road data:", error);
      setRoadData(null);
    }
  };

  

  return (
    <>
      <div className="flex justify-between h-screen">
        <div className="w-16 h-screen border-r flex flex-col justify-between">
          <div>
            <div className="flex h-16 items-center px-4 border-b">
              <Logo />
            </div>
            <div className="flex flex-col items-center my-4 space-y-4">
              <MainNav />
            </div>
          </div>
          <div className="flex flex-col items-center my-4 space-y-4">
            <UserNav />
          </div>
        </div>

        <div className="flex-grow">
          <Tabs defaultValue="map" className="w-auto">
            <div className="h-16 flex items-center justify-between border-b px-4">
              <h1 className="text-xl font-bold">Overview</h1>

              <div className="flex items-center space-x-2">
                <ThemeToggle />
                <TabsList>
                  <TabsTrigger value="map">Map</TabsTrigger>
                  <TabsTrigger value="info">Info</TabsTrigger>
                </TabsList>
              </div>
            </div>

            <div className="flex-grow h-full w-full">
              <TabsContent value="map" className="w-full h-full p-0 m-0">
                {/* Map Component */}
              </TabsContent>
              <TabsContent value="info" className="w-full h-full p-0 m-0">
                {selectedRoad ? (
                  // Display dashboard with road data
                  <Dashboard roadData={roadData}>
                    <video src={videoUrl} className="rounded-lg shadow-lg w-full h-64"></video>
                  </Dashboard>
                ) : (
                  <p>No road selected</p>
                )}
              </TabsContent>
            </div>
          </Tabs>
        </div>

        <div className="w-96 h-screen border-l">
          <div className="flex h-16 items-center border-b px-4">
            <SearchBar onSearch={handleSearch} className="flex-grow" />
          </div>
          <RoadList
            searchTerm={searchTerm}
            selectedCity={selectedCity}
            onRoadSelect={handleRoadSelect} // Pass handler to RoadList
          />
        </div>
      </div>
    </>
  );
}
