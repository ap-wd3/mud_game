import React, { useEffect, useState, useRef } from "react";
import {
  AppRegistry,
  SafeAreaView,
  TouchableOpacity,
  StyleSheet,
  Text,
  View,
  Animated,
} from "react-native";
import AsyncStorage from "@react-native-async-storage/async-storage";
import { Dangrek_400Regular } from "@expo-google-fonts/dangrek";
import { useFonts } from "expo-font";
import axios from 'axios';
import { ChevronLeftIcon } from 'react-native-heroicons/solid';

export default function Game(props) {
  const navigation = props.navigation;
  const { user_id, username, email, categoryName, wordSetId, wordSetName, img } = props.route.params;
  const [shuffledFlashcards, setShuffledFlashcards] = useState([]);
  const [selectedCards, setSelectedCards] = useState([]);
  const [matchedCards, setMatchedCards] = useState([]);
  const [mismatchedCards, setMismatchedCards] = useState([]); //this
  const [timer, setTimer] = useState(0);
  const [isTimerRunning, setIsTimerRunning] = useState(false);
  const timerRef = useRef(null);
  const lastTimeRef = useRef(0);
  const [fontsLoaded] = useFonts({
    Dangrek_400Regular,
  });

  useEffect(() => {
    const fetchFlashcards = async () => {
      try {
        const response = await axios.get(`https://exciting-monster-living.ngrok-free.app/flashcards/${wordSetId}`);
        const combinedFlashcards = response.data.flatMap(card => [
          { id: `${card.english_word}-${card.thai_word}`, type: 'english', text: card.english_word },
          { id: `${card.english_word}-${card.thai_word}`, type: 'thai', text: card.thai_word, pronunciation: card.pronunciation }
        ]);
        setShuffledFlashcards(shuffleArray(combinedFlashcards));
      } catch (error) {
        console.error(error);
      }
    };

    fetchFlashcards();

    return () => clearInterval(timerRef.current);
  }, [wordSetId]);

  useEffect(() => {
    let animationFrameId;
  
    const animate = () => {
      const now = Date.now();
      const deltaTime = now - lastTimeRef.current;
      lastTimeRef.current = now;
  
      if (isTimerRunning) {
        setTimer(prev => prev + deltaTime);
        animationFrameId = requestAnimationFrame(animate);
      }
    };
  
    if (isTimerRunning) {
      lastTimeRef.current = Date.now();
      animationFrameId = requestAnimationFrame(animate);
    } else {
      lastTimeRef.current = 0;
    }
  
    return () => cancelAnimationFrame(animationFrameId);
  }, [isTimerRunning]);

  const resetGame = () => {
    setSelectedCards([]);
    setMatchedCards([]);
    setMismatchedCards([]);
    setTimer(0);
    setIsTimerRunning(false);
    lastTimeRef.current = 0;
  };

  const handleCardPress = (index) => {
    if (!isTimerRunning) {
      setIsTimerRunning(true);
    }
  
    if (matchedCards.some(card => card.index === index && card.matched)) {
      return;
    }
  
    if (selectedCards.length < 2 && !selectedCards.includes(index)) {
      const newSelectedCards = [...selectedCards, index];
      setSelectedCards(newSelectedCards);
  
      if (newSelectedCards.length === 2) {
        const firstCard = shuffledFlashcards[newSelectedCards[0]];
        const secondCard = shuffledFlashcards[newSelectedCards[1]];
  
        if (firstCard.id === secondCard.id && firstCard.type !== secondCard.type) {
          setMatchedCards(prev => [...prev, ...newSelectedCards]);
  
          if (matchedCards.length + 2 === shuffledFlashcards.length) {
            handleGameFinish();
          }
  
          setSelectedCards([]);
        } else {
          setMismatchedCards(newSelectedCards);
          setTimeout(() => {
            setMismatchedCards([]);
            setSelectedCards([]);
          }, 50);
        }
      }
    }
  };

  const handleGameFinish = () => {
    setIsTimerRunning(false);
    const formattedTime = formatTime(timer);

    axios.post('https://exciting-monster-living.ngrok-free.app/game', {
      user_id: user_id,
      word_set_id: wordSetId,
      finished_time: formattedTime
    })
    .then(response => {
      console.log('Leaderboard updated:', response.data);
      resetGame();
      navigation.navigate('Leaderboard', { user_id, username, email, categoryName, wordSetId, wordSetName, img});
    })
    .catch(error => {
      console.error('Error updating leaderboard:', error);
    });
  };

  const formatTime = (milliseconds) => {
    const mins = Math.floor(milliseconds / 60000);
    const secs = Math.floor((milliseconds % 60000) / 1000);
    const millis = Math.floor((milliseconds % 1000) / 10);
    return `${mins.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}:${millis.toString().padStart(2, '0')}`;
  };

  const shuffleArray = (array) => {
    for (let i = array.length - 1; i > 0; i--) {
      const j = Math.floor(Math.random() * (i + 1));
      [array[i], array[j]] = [array[j], array[i]];
    }
    return array;
  };

  const getCardStyle = (index) => {
    const card = shuffledFlashcards[index];
    const cardWidth = card.text.length > 19 ? { width: 198 } : {};
    const cardPadding = card.text.length > 19 ? { paddingHorizontal: 16 } : {};

    if (matchedCards.includes(index)) {
      return { ...styles.card, ...styles.matchedCard, ...cardWidth, ...cardPadding };
    }
    if (mismatchedCards.includes(index)) {
      return { ...styles.card, ...styles.animatingCard, ...cardWidth, ...cardPadding };
    }
    return { ...styles.card, ...cardWidth, ...cardPadding };
  };

  if (!fontsLoaded) {
    return <Text>Font Loading...</Text>;
  }
  return (
    <SafeAreaView className="flex-1 bg-[#397CE1]">
      <View className="flex-row h-20 px-4 mb-8 items-center justify-center">
        <TouchableOpacity onPress={() => navigation.goBack()} className="ml-5 absolute left-0 bg-white rounded-full p-3 shadow">
          <ChevronLeftIcon size={23} stroke={50} color="#434343" />
        </TouchableOpacity>
        <Text className="font-[dangrek] text-white pt-8 text-4xl">
          {categoryName}
        </Text>
        <Text className="absolute pt-20 font-[dangrek] text-white text-lg">
            {wordSetName}
        </Text>
      </View>
      <View className="flex-1 bg-[#CCE0FF] items-center pt-10">
        <Text className="mb-5 font-[dangrek] text-3xl pt-1 text-black text-center shadow-sm">
          {formatTime(timer)}
        </Text>
        <View className=" justify-center">
          <View className="flex-row flex-wrap justify-center ml-[-8px]">
          {shuffledFlashcards.slice(0, 20).map((card, index) => (
            <TouchableOpacity
              key={index}
              onPress={() => handleCardPress(index)}
              style={getCardStyle(index)}
              className="bg-white w-24 h-24 mb-2 ml-2 justify-center items-center shadow-sm rounded-xl"
            >
              {card.type === 'english' ? (
                <Text className="font-[dangrek] text-xl pt-2">{card.text}</Text>
              ) : (
                <>
                  <Text className="text-base">{card.text}</Text>
                  <Text className="text-base">{card.pronunciation}</Text>
                </>
              )}
            </TouchableOpacity>
          ))}
        </View>
        </View>
      </View>
    </SafeAreaView>
    );
  }

  const styles = StyleSheet.create({
    matchedCard: {
      borderColor: 'green', // Green border for matched cards
      borderWidth: 8,
      pointerEvents: 'none',
      opacity: 0, // Hidden when matched
    },
    animatingCard: {
      borderColor: 'red', // Red border for mismatched cards during animation
      borderWidth: 8,
      opacity: 0.5, // Reduced opacity during animation
    },
  });

AppRegistry.registerComponent("Game", () => Game);