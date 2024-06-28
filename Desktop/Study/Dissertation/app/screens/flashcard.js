import React, { useEffect, useState, useRef } from "react";
import {
  AppRegistry,
  SafeAreaView,
  TouchableOpacity,
  StyleSheet,
  Text,
  View,
  Animated,
  Dimensions,
} from "react-native";
import AsyncStorage from "@react-native-async-storage/async-storage";
import { Dangrek_400Regular } from "@expo-google-fonts/dangrek";
import { useFonts } from "expo-font";
import axios from 'axios';
import { ArrowPathIcon, ChevronLeftIcon, ChartBarIcon} from 'react-native-heroicons/solid';
import { PanGestureHandler, GestureHandlerRootView, State } from 'react-native-gesture-handler';
import { widthPercentageToDP as wp, heightPercentageToDP as hp } from 'react-native-responsive-dimensions';

export default function Flashcard(props) {
  const navigation = props.navigation;
  const { user_id, username, email, categoryName, wordSetId, wordSetName, img } = props.route.params;
  const [flashcards, setFlashcards] = useState([]);
  const [currentCard, setCurrentCard] = useState(0);
  const position = useRef(new Animated.ValueXY()).current;
  const flipAnimation = useRef(new Animated.Value(0)).current;
  const [flipped, setFlipped] = useState(false);
  const [fontsLoaded] = useFonts({
    Dangrek_400Regular,
  });
  const [initialFlashcards, setInitialFlashcards] = useState([]);
  const card = flashcards[currentCard];

  useEffect(() => {
    const fetchFlashcards = async () => {
        try {
            const response = await axios.get(`https://exciting-monster-living.ngrok-free.app/flashcards/${wordSetId}`);
            setFlashcards(response.data);
            setInitialFlashcards(response.data); // Save the initial set of flashcards
        } catch (error) {
            console.error(error);
        }
    };

    fetchFlashcards();
  }, [wordSetId]);

  const handleFlip = () => {
    Animated.timing(flipAnimation, {
      duration: 300,
      toValue: flipped ? 0 : 180,
      useNativeDriver: true,
    }).start();
    setFlipped(!flipped);
  };

  const interpolateFront = flipAnimation.interpolate({
    inputRange: [0, 180],
    outputRange: ['0deg', '180deg'],
  });

  const interpolateBack = flipAnimation.interpolate({
    inputRange: [0, 180],
    outputRange: ['180deg', '360deg'],
  });

  const handleSwipe = (event) => {
    const translationX = event.nativeEvent.translationX;
    const threshold = 100; // Adjust the threshold as needed

    if (translationX < -threshold) {
      // Swiped left
      setCurrentCard((prevCard) => (prevCard + 1) % flashcards.length);
      setFlipped(false);
      flipAnimation.setValue(0);
    } else if (translationX > threshold) {
      // Swiped right
      setFlashcards((prevFlashcards) => {
        const updatedFlashcards = prevFlashcards.slice(1);
        setCurrentCard(0); // Reset to first card or adjust accordingly
        return updatedFlashcards;
      });
      setFlipped(false);
      flipAnimation.setValue(0);
    } else {
      // Reset position if within threshold
      Animated.spring(position, {
        toValue: { x: 0, y: 0 },
        useNativeDriver: true,
      }).start();
      return; // Exit without updating the current card index
    }

    // Reset the position after updating the current card
    Animated.spring(position, {
      toValue: { x: 0, y: 0 },
      useNativeDriver: true,
    }).start();
  };

  const handlePanGesture = Animated.event(
    [{ nativeEvent: { translationX: position.x, translationY: position.y } }],
    { useNativeDriver: false }
  );

  const borderColor = position.x.interpolate({
    inputRange: [-200, 0, 200],
    outputRange: ['yellow', 'transparent', 'green'],
  });

  const practiceMoreOpacity = position.x.interpolate({
    inputRange: [-200, -100],
    outputRange: [1, 0],
    extrapolate: 'clamp',
  });

  const learnedOpacity = position.x.interpolate({
    inputRange: [100, 200],
    outputRange: [0, 1],
    extrapolate: 'clamp',
  });

  const handleReplay = () => {
    setFlashcards(initialFlashcards);
    setCurrentCard(0);
    Animated.spring(position, {
      toValue: { x: 0, y: 0 },
      useNativeDriver: true,
    }).start();
  };

  if (!fontsLoaded) {
    return <Text>Font Loading...</Text>;
  }

  return (
    <GestureHandlerRootView style={{ flex: 1 }}>
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
        <View className="flex-0 bg-[#CCE0FF] items-center pt-10">
          <View className="w-80 h-[132vw] relative mb-10">
            {flashcards.length > 0 ? (
              card && (
                <TouchableOpacity onPress={handleFlip} style={styles.card}>
                  <PanGestureHandler
                    onGestureEvent={handlePanGesture}
                    onHandlerStateChange={(event) => {
                      if (event.nativeEvent.state === State.END) {
                        handleSwipe(event);
                      }
                    }}
                  >
                    <Animated.View
                      style={[
                        { transform: [{ translateX: position.x }, { translateY: position.y }] },
                        styles.card,
                      ]}
                    >
                      <Animated.View style={[styles.topBanner, styles.practiceMoreBanner, { opacity: practiceMoreOpacity }]}>
                        <Text className="font-[dangrek] text-black text-3xl mt-4 pt-1">need more times</Text>
                      </Animated.View>
                      <Animated.View style={[styles.topBanner, styles.learnedBanner, { opacity: learnedOpacity }]}>
                        <Text className="font-[dangrek] text-white text-3xl mt-4 pt-1">ok!</Text>
                      </Animated.View>
                      <Animated.View style={[
                          styles.animatedBorder,
                          { borderColor: borderColor, borderWidth: 10 }
                        ]} />
                      <Animated.View
                        style={[
                          { transform: [{ rotateY: interpolateFront }] },
                          styles.card,
                          flipped ? styles.hidden : null
                        ]}>
                        <View className="bg-white w-[100%] h-[100%] mb-10 justify-center items-center shadow-sm rounded-xl">
                          <Text className="font-[dangrek] text-5xl pt-5">{card.english_word}</Text>
                        </View>
                      </Animated.View>
                      <Animated.View
                        style={[
                          { transform: [{ rotateY: interpolateBack }] },
                          styles.card,
                          !flipped ? styles.hidden : null
                        ]}>
                        <View className="bg-white w-80 h-[132vw] mb-10 justify-center items-center shadow-sm rounded-xl">
                          <Text className="text-5xl pt-3 mb-5">{card.thai_word}</Text>
                          <Text className="text-5xl">{card.pronunciation}</Text>
                        </View>
                      </Animated.View>
                    </Animated.View>
                  </PanGestureHandler>
                </TouchableOpacity>
              )
            ) : (
              <View className="w-80 h-[132vw] justify-center items-center">
                <Text className="font-[dangrek] text-5xl pt-4">No more cards!</Text>
                <TouchableOpacity onPress={handleReplay} className="ml-5 left-0 bg-white rounded-full p-3 shadow">
                  <ArrowPathIcon size={40} stroke={50} color="#434343" />
                </TouchableOpacity>
              </View>
            )}
          </View>
          <View className="flex-row justify-between mb-12">
            <Text className="font-[dangrek] text-3xl w-30 pt-7 ml-9">{flashcards.length > 0 ? currentCard + 1 : 0}/{flashcards.length > 0 ? flashcards.length : initialFlashcards.length}</Text>
            <TouchableOpacity onPress={() => navigation.navigate('Game', { user_id: user_id, username: username, email: email, categoryName: categoryName, wordSetId: wordSetId, wordSetName: wordSetName, img: img })} className="bg-[#397CE1] w-[180px] py-3 rounded-xl items-center ml-12">
              <Text className="font-[dangrek] text-white pt-4 text-3xl">Play!</Text>
            </TouchableOpacity>
          </View>
        </View>
      </SafeAreaView>
    </GestureHandlerRootView>
  );
}

const styles = StyleSheet.create({
  hidden: {
    opacity: 0,
  },
  card: {
    backfaceVisibility: 'hidden',
    position: 'absolute',
    width: '100%',
    height: '100%',
    borderRadius: 10,
  },
  topBanner: {
    position: 'absolute',
    top: 0,
    width: '100%',
    paddingVertical: 10,
    alignItems: 'center',
    zIndex: 1,
  },
  practiceMoreBanner: {
    backgroundColor: 'yellow',
  },
  learnedBanner: {
    backgroundColor: 'green',
  },
  animatedBorder: {
    position: 'absolute',
    width: '100%',
    height: '100%',
    borderRadius: 10,
    zIndex: 2,
  }
});

AppRegistry.registerComponent("Flashcard", () => Flashcard);