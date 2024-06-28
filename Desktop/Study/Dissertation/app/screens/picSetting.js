import React, { useEffect, useState } from "react";
import { AppRegistry, SafeAreaView, TouchableOpacity, Image, Text, View } from "react-native";
import { ChevronLeftIcon } from 'react-native-heroicons/solid';
import { Dangrek_400Regular } from "@expo-google-fonts/dangrek";
import { useFonts } from "expo-font";
import axios from 'axios';

export default function PicSetting(props) {
  const navigation = props.navigation;
  const [currentProfilePic, setCurrentProfilePic] = useState(require('../assets/user-default.png')); // Initial profile picture
  const profilePics = [
    { src: require('../assets/user-default.png'), filename: 'user-default.png' },
    { src: require('../assets/user1.png'), filename: 'user1.png' },
    { src: require('../assets/user3.png'), filename: 'user3.png' },
    { src: require('../assets/user4.png'), filename: 'user4.png' },
    { src: require('../assets/user5.png'), filename: 'user5.png' },
    { src: require('../assets/user6.png'), filename: 'user6.png' },
    { src: require('../assets/user7.png'), filename: 'user7.png' },
  ];

  let [fontsLoaded] = useFonts({
    Dangrek_400Regular,
  });

  const handleImageTap = async (pic) => {
    try {
      const { email } = props.route.params;
      const filename = pic.filename;
  
      setCurrentProfilePic(pic.src); // Update the current profile picture state with the selected image
      
      console.log('pic.filename', pic.filename)
      console.log('pic.src', pic.src)
      // Send a PUT request to update the profile picture on the server
      await axios.put('https://exciting-monster-living.ngrok-free.app/updatePic', {
        email: email,
        img: filename // Pass only the filename to the backend
      });

      // Optionally, navigate back after successful update
      navigation.goBack();
    } catch (error) {
      console.error('Error updating profile picture:', error);
      // Handle error scenarios, e.g., show a message to the user
    }
  };

  if (!fontsLoaded) {
    return <Text>Font Loading...</Text>;
  }
  return (
    <SafeAreaView className="flex-1 bg-[#397CE1]">
      <View className="bg-[#397CE1] h-20 px-4 mb-5 items-center justify-center">
        <TouchableOpacity onPress={() => navigation.goBack()} className="absolute left-0 ml-5 bg-white rounded-full p-3 shadow">
          <ChevronLeftIcon size={23} stroke={50} color="#434343" />
        </TouchableOpacity>
        <Text className="font-[dangrek] text-white pt-8 text-4xl">Change Picture</Text>
      </View>
      <View className="flex-1 bg-[#CCE0FF] flex-row flex-wrap items-center px-5 justify-center pt-10">
      {profilePics.map((pic, index) => (
        <TouchableOpacity key={index} 
          className="my-2" 
          onPress={() => handleImageTap(pic)}
        >
          <Image source={pic.src} className="w-32 h-32" />
        </TouchableOpacity>
      ))}
        </View>
    </SafeAreaView>
  );
}

AppRegistry.registerComponent("PicSetting", () => PicSetting);