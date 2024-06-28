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
import { Dangrek_400Regular } from "@expo-google-fonts/dangrek";
import { useFonts } from "expo-font";
import axios from 'axios';
import { ChevronLeftIcon } from 'react-native-heroicons/solid';

export default function SetSelect(props) {
  const navigation = props.navigation;
  const { user_id, username, email, categoryId, categoryName, img, type } = props.route.params;
  const [wordSet, setWordSet] = useState([]);
  const [fontsLoaded] = useFonts({
    Dangrek_400Regular,
  });

  useEffect(() => {
    const fecthWordSet = async () => {
        try {
            const response = await axios.get(`https://exciting-monster-living.ngrok-free.app/wordSet/${categoryId}`);
            setWordSet(response.data);
        } catch (error) {
            console.error(error);
        }
    };

    fecthWordSet();
  }, []);

  if (!fontsLoaded) {
    return <Text>Font Loading...</Text>;
  }
  return (
    <SafeAreaView className="flex-1 bg-[#397CE1]">
      <View className="flex-row h-20 px-4 mb-5 items-center justify-center">
        <TouchableOpacity onPress={() => navigation.goBack()} className="ml-5 absolute left-0 bg-white rounded-full p-3 shadow">
          <ChevronLeftIcon size={23} stroke={50} color="#434343" />
        </TouchableOpacity>
        <Text className="font-[dangrek] text-white pt-8 text-4xl">
          {categoryName}
        </Text>
      </View>
      <View className="flex-1 bg-[#CCE0FF] justify-center items-center pt-8">
        <Text className="mb-5 font-[dangrek] text-3xl text-white text-center shadow-sm pt-1">Please select the word set</Text>
        <FlatList
                data={wordSet}
                keyExtractor={item => item.id.toString()}
                renderItem={({ item }) => (
                  <TouchableOpacity onPress={() => {
                    if (type === 'admin') {
                      navigation.navigate('WordDict', {
                        user_id: user_id,
                        username: username,
                        email: email,
                        categoryName: categoryName,
                        wordSetId: item.id,
                        wordSetName: item.name,
                        img: img
                      });
                    } else if (type === 'player') {
                      navigation.navigate('Flashcard', {
                        user_id: user_id,
                        username: username,
                        email: email,
                        categoryName: categoryName,
                        wordSetId: item.id,
                        wordSetName: item.name,
                        img: img
                      });
                    }
                  }}
                  className="bg-white w-[80vw] h-32 mb-5 justify-center items-center shadow-sm rounded-xl"
                >
                        <Text className="font-[dangrek] text-4xl mt-4 p-10">{item.name}</Text>
                    </TouchableOpacity>
                )}
        />
      </View>
    </SafeAreaView>
  );
}


AppRegistry.registerComponent("SetSelect", () => SetSelect);