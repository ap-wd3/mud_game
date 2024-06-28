import React, { useEffect, useState, useCallback } from "react";
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
import { useFocusEffect } from "@react-navigation/native";
import AsyncStorage from "@react-native-async-storage/async-storage";
import { Dangrek_400Regular } from "@expo-google-fonts/dangrek";
import { useFonts } from "expo-font";
import axios from 'axios';
import { ChevronLeftIcon } from 'react-native-heroicons/solid';
import SearchInput, { createFilter } from 'react-native-search-filter';

export default function WordDict(props) {
  const navigation = props.navigation;
  const { user_id, username, email, categoryName, wordSetId, wordSetName, img } = props.route.params;
  const [categories, setCategories] = useState([]);
  const [fontsLoaded] = useFonts({
    Dangrek_400Regular,
  });

  if (!fontsLoaded) {
    return <Text>Font Loading...</Text>;
  }
  return (
    <SafeAreaView className="flex-1 bg-[#397CE1]">
        <View className="flex-row px-4 items-center justify-center">
            <TouchableOpacity onPress={() => navigation.goBack()} 
            className="ml-5 absolute left-0 bg-white rounded-full p-3 shadow">
                <ChevronLeftIcon size={23} stroke={50} color="#434343" />
            </TouchableOpacity>
            <Text className="font-[dangrek] text-white pt-8 text-4xl">
            {categoryName}
            </Text>
            <TouchableOpacity onPress={() => navigation.navigate('Leaderboard', { user_id, username, email, categoryName, wordSetId, wordSetName, img})} 
            className="mr-5 absolute right-0 p-3">
                <ChartBarIcon size={30} color="#ffffff"/>
            </TouchableOpacity>
        </View>
        <View className="items-center justify-center px-4 mb-5 mt-[-2vw]">
          <Text className="font-[dangrek] text-white text-lg">
              {wordSetName}
          </Text>
        </View>
      <View className="flex-1 bg-[#CCE0FF] justify-center items-center pt-8">
        <SearchInput className="mb-5 font-[dangrek] text-3xl pt-1 text-white text-center shadow-sm"/>
        <FlatList
                data={categories}
                keyExtractor={item => item.id.toString()}
                renderItem={({ item }) => (
                    <TouchableOpacity 
                      onPress={() => navigation.navigate('SetSelect', { user_id: user_id, username: username, email: email, categoryId: item.id, categoryName: item.name, img:img, type:type })} 
                      className="bg-white w-[80vw] h-32 mb-5 justify-center items-center shadow-sm rounded-xl">
                        <Text className="font-[dangrek] text-4xl mt-4 p-10">{item.name}</Text>
                    </TouchableOpacity>
                )}
        />
      </View>
    </SafeAreaView>
  );
}


AppRegistry.registerComponent("WordDict", () => WordDict);