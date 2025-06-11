import React, { useState } from "react";
import { Card, CardContent } from "@/components/ui/card";
import { RadioGroup, RadioGroupItem } from "@/components/ui/radio-group";
import { Label } from "@/components/ui/label";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";

export default function ChatRTXUI() {
  const [selectedOption, setSelectedOption] = useState("option1");
  const [systemPath, setSystemPath] = useState("");

  const handleRadioChange = (value) => {
    setSelectedOption(value);
  };

  const handlePathChange = (e) => {
    setSystemPath(e.target.value);
  };

  const handleSubmit = () => {
    console.log("Selected Option:", selectedOption);
    console.log("System Path:", systemPath);
  };

  return (
    <div className="p-6 max-w-md mx-auto">
      <Card className="rounded-2xl shadow-md">
        <CardContent className="p-6">
          <h2 className="text-xl font-semibold mb-4">Chat RTX Configuration</h2>
          <div className="mb-4">
            <Label className="block mb-2">Choose an option:</Label>
            <RadioGroup
              value={selectedOption}
              onValueChange={handleRadioChange}
              className="space-y-2"
            >
              <div className="flex items-center space-x-2">
                <RadioGroupItem value="option1" id="option1" />
                <Label htmlFor="option1">Option 1</Label>
              </div>
              <div className="flex items-center space-x-2">
                <RadioGroupItem value="option2" id="option2" />
                <Label htmlFor="option2">Option 2</Label>
              </div>
              <div className="flex items-center space-x-2">
                <RadioGroupItem value="option3" id="option3" />
                <Label htmlFor="option3">Option 3</Label>
              </div>
            </RadioGroup>
          </div>

          <div className="mb-4">
            <Label htmlFor="systemPath" className="block mb-2">System Path:</Label>
            <Input
              id="systemPath"
              type="text"
              value={systemPath}
              onChange={handlePathChange}
              placeholder="Enter your system path"
            />
          </div>

          <Button className="w-full" onClick={handleSubmit}>Submit</Button>
        </CardContent>
      </Card>
    </div>
  );
}
