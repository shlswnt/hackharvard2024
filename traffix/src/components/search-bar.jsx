"use client";

import { useState, useEffect } from "react";
import { Input } from "@/components/ui/input";
import {
  Select,
  SelectContent,
  SelectGroup,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import { Separator } from "@/components/ui/separator";

export function SearchBar({ className, onSearch }) {
  const [searchTerm, setSearchTerm] = useState("");
  const [selectedCity, setSelectedCity] = useState("all");

  const handleSearchChange = (e) => {
    setSearchTerm(e.target.value);
    onSearch(e.target.value, selectedCity);
  };

  const handleCityChange = (value) => {
    setSelectedCity(value);
    onSearch(searchTerm, value);
  };

  useEffect(() => {
    onSearch(searchTerm, selectedCity);
  }, [selectedCity, searchTerm, onSearch]);

  return (
    <div className={`flex items-center space-x-2 ${className}`}>
      <Input
        type="text"
        placeholder="Search roads..."
        value={searchTerm}
        onChange={handleSearchChange}
        className="flex-grow"
      />
      <Select value={selectedCity} onValueChange={handleCityChange}>
        <SelectTrigger className="w-48">
          <SelectValue placeholder="All Cities" />
        </SelectTrigger>
        <SelectContent>
          <SelectGroup>
            <SelectItem value="all">All Cities</SelectItem>
            <Separator />
            <SelectItem value="at">Atlanta</SelectItem>
            <SelectItem value="lv">Las Vegas</SelectItem>
            <SelectItem value="ny">Manhattan</SelectItem>
          </SelectGroup>
        </SelectContent>
      </Select>
    </div>
  );
}
