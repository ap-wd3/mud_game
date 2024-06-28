import React, { useEffect, useState } from "react";
import {
  AppRegistry,
  SafeAreaView,
  TouchableOpacity,
  FlatList,
  Image,
  StyleSheet,
  Text,
  View,
} from "react-native";
import AsyncStorage from "@react-native-async-storage/async-storage";
import { Dangrek_400Regular } from "@expo-google-fonts/dangrek";
import { useFonts } from "expo-font";
import axios from 'axios';
import { ArrowPathIcon } from 'react-native-heroicons/solid';


export default function TopicSelect(props) {
  const navigation = props.navigation;
  const { user_id, username, email, categoryName, wordSetId, wordSetName, img } = props.route.params;
  const [leaderboard, setLeaderboard] = useState([]);
  const [fontsLoaded] = useFonts({
    Dangrek_400Regular,
  });
  const imageSources = {
    'user-default.png': require('../assets/user-default.png'),
    'user1.png': require('../assets/user1.png'),
    'user2.png': require('../assets/user2.png'),
    'user3.png': require('../assets/user3.png'),
    'user4.png': require('../assets/user4.png'),
    'user5.png': require('../assets/user5.png'),
    'user6.png': require('../assets/user6.png'),
    'user7.png': require('../assets/user7.png'),
  }

  useEffect(() => {
    const fetchLeaderboard = async () => {
      try {
        const response = await axios.get(`https://exciting-monster-living.ngrok-free.app/leaderboard/${wordSetId}`);
        setLeaderboard(response.data);
      } catch (error) {
        console.error('Error fetching leaderboard:', error);
      }
    };

    fetchLeaderboard();
  }, []);

  if (!fontsLoaded) {
    return <Text>Font Loading...</Text>;
  }
  return (
    <SafeAreaView className="flex-1 bg-[#397CE1]">
      <View className="h-20 px-4 mb-12 items-center">
        {img ? (
          <Image source={imageSources[img]} className="w-20 h-20 mb-2"/>
        ) : (
        <Image source={require('../assets/user-default.png')} className="w-20 h-20 mb-2"/>
        )}
        <Text className="font-[dangrek] text-white text-xl">
          {`Good Job, ${username ? username : '...'}!`}
        </Text>
      </View>
      <View className="flex-1 bg-[#CCE0FF] pt-5">
        <View className="justify-center items-center mb-2">
          <Text className="font-[dangrek] text-white shadow-sm text-6xl pt-6 mb-[-4vw]">Leaderbord</Text>
          <Text className="font-[dangrek] text-white shadow-sm text-3xl pt-1">{categoryName} - {wordSetName}</Text>
        </View>
        <View className="flex-1 px-6">
        <FlatList
        data={leaderboard}
        keyExtractor={(item) => item.rank.toString()}
        renderItem={({ item }) => (
          <View className="flex-row items-center px-2">
            <Text className="font-[dangrek] text-3xl items-center flex-1 pt-2">{item.rank}</Text>
            <Image
                  source={imageSources[item.img] || imageSources['user-default.png']}
                  className="w-20 h-20 mb-2 ml-[-120px]"
                />
            <Text className="font-[dangrek] text-xl items-center flex-1 ml-4">{item.username}</Text>
            <Text className="font-[dangrek] text-xl items-center">{item.finished_time}</Text>
          </View>
          )}
        />
        </View>
        <View className="flex-row space-x-5 justify-center items-center mb-5">
        <TouchableOpacity 
          onPress={() => navigation.navigate('Game', { user_id: user_id, username: username, categoryName: categoryName, wordSetId: wordSetId, wordSetName: wordSetName, img: img })}
          className="bg-[#397CE1] rounded-lg w-36 h-20 justify-center items-center"
        >
          <ArrowPathIcon size={40} stroke={50} color="#fff" />
        </TouchableOpacity>
        <TouchableOpacity 
          onPress={() => navigation.navigate('TopicSelect', { user_id: user_id, username: username, email: email })}
          className="bg-[#3EC928] rounded-lg w-36 h-20 justify-center items-center"
        >
          <Text className="font-[dangrek] text-white text-5xl pt-9">Done</Text>
        </TouchableOpacity>
        </View>
      </View>
    </SafeAreaView>
  );
}

AppRegistry.registerComponent("Leaderboard", () => Leaderboard);