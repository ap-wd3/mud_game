import React, { useEffect, useState, useRef, useCallback } from "react";
import {
  AppRegistry,
  SafeAreaView,
  TouchableOpacity,
  TextInput,
  StyleSheet,
  Image,
  Text,
  View,
} from "react-native";
import { Dangrek_400Regular } from "@expo-google-fonts/dangrek";
import { useFonts } from "expo-font";
import axios from 'axios';
import { useFocusEffect } from '@react-navigation/native';
import validation from "../validations/updateValidation";
import { ChevronLeftIcon, PencilSquareIcon } from 'react-native-heroicons/solid';

export default function User(props) {
  const navigation = props.navigation;
  const { username: initialUsername, email: initialEmail, password: initialPassword, img: initialImg } = props.route.params;
  const [fontsLoaded] = useFonts({ Dangrek_400Regular });
  const [editMode, setEditMode] = useState({ username: false, email: false, password: false });
  const [username, setUsername] = useState(initialUsername);
  const [email, setEmail] = useState(initialEmail);
  const [password, setPassword] = useState(initialPassword);
  const [img, setImg] = useState(initialImg);
  const [showSaveCancel, setShowSaveCancel] = useState(false);
  const [errors, setErrors] = useState({});
  const [usernameChanged, setUsernameChanged] = useState(false);
  const [passwordChanged, setPasswordChanged] = useState(false);

  const usernameInputRef = useRef(null);
  const passwordInputRef = useRef(null);

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

  const handleEditToggle = (field) => {
    setEditMode((prevState) => ({ ...prevState, [field]: !prevState[field] }));
    setShowSaveCancel(true);
  
    if (field === 'username') {
      setUsernameChanged(true);
      setTimeout(() => {
        usernameInputRef.current.focus();
      }, 100);
    } else if (field === 'password') {
      setPasswordChanged(true);
      setTimeout(() => {
        passwordInputRef.current.focus();
      }, 100);
    }
  };

  const handleUpdate = async () => {
    const err = validation({ username, password });
  
    if (editMode.password) {
      setErrors(err);
    } else {
      setErrors({ username: err.username, password: "" }); // Clear password error if not editing
    }
  
    if (err.username === "" && (!passwordChanged || err.password === "")) {
      try {
        let updatedData = { email: email };
  
        if (usernameChanged) {
          updatedData.username = username;
        }
        if (passwordChanged) {
          updatedData.password = password;
        }
  
        await axios.put('https://exciting-monster-living.ngrok-free.app/updateUser', updatedData);
        setEditMode({ username: false, password: false });
        setShowSaveCancel(false);
        setUsernameChanged(false);
        setPasswordChanged(false);
      } catch (error) {
        console.error('Error updating user:', error);
      }
    }
  };

  const handleCancel = () => {
    setUsername(initialUsername);
    setPassword(initialPassword);
    setEditMode({ username: false, email: false, password: false });
    setShowSaveCancel(false);
    setErrors({}); 
  };

  useFocusEffect(
    useCallback(() => {
      // Fetch or update profile picture state when the screen is focused
      const fetchUserData = async () => {
        try {
          const response = await axios.get(`https://exciting-monster-living.ngrok-free.app/getUser`, { params: { email } });
          setImg(response.data.img);
        } catch (error) {
          console.error('Error fetching user data:', error);
        }
      };

      fetchUserData();
    }, [])
  );

  if (!fontsLoaded) {
    return <Text>Font Loading...</Text>;
  }
  return (
    <SafeAreaView className="flex-1 bg-[#397CE1]">
      <View className="bg-[#397CE1] h-20 px-4 mb-5 items-center justify-center">
        <TouchableOpacity onPress={() => navigation.goBack()} className="absolute left-0 ml-5 bg-white rounded-full p-3 shadow">
          <ChevronLeftIcon size={23} stroke={50} color="#434343" />
        </TouchableOpacity>
        <Text className="font-[dangrek] text-white pt-8 text-4xl">Profile Setting</Text>
      </View>
      <View className="flex-1 bg-[#CCE0FF] items-center">
        <TouchableOpacity  onPress={() => navigation.navigate('PicSetting', {email: email, img: img})} className="my-5">
          {img ? (
          <Image source={imageSources[img]} className="h-40 w-40"/>
          ) : (
            <Image source={require('../assets/user-blank.png')} className="h-40 w-40"/>
          )}
          </TouchableOpacity>
        <View className="flex-row items-center px-5 mb-5">
          <Text className="flex-1 font-[dangrek] text-2xl pt-3">Username</Text>
          <TextInput
            ref={usernameInputRef}
            className={`font-[dangrek] text-2xl bg-white rounded-2xl w-60 h-16 pt-6 pl-4 ${editMode.username ? 'text-black' : 'text-stone-500'}`}
            name="name"
            placeholder='username'
            placeholderTextColor="rgba(0,0,0,0.5)"
            returnKeyType="next"
            keyboardType="go"
            autoCapitalize="none"
            autoCorrect={false}
            value={username}
            editable={editMode.username}
            onChangeText={setUsername}
          />
          <TouchableOpacity
            onPress={() => editMode.username ? handleUpdate() : handleEditToggle('username')}
            className="justify-center items-center bg-white rounded-r-2xl w-16 h-16 ml-[-65px]"
          >
            <PencilSquareIcon size={23} stroke={50} color="#000000" />
          </TouchableOpacity>
        </View>
        {errors.username && <Text style={styles.text}>{errors.username}</Text>}
        <View className="flex-row items-center px-5 mb-5">
          <Text className="flex-1 font-[dangrek] pt-3 text-2xl">Email</Text>
          <TextInput
            className="font-[dangrek] text-stone-500 text-2xl bg-white rounded-2xl w-60 h-16 pt-5 pl-4"
            name="email"
            editable={false}
            value={email}
          />
        </View>
        <View className="flex-row items-center px-5 mb-10">
          <Text className="flex-1 font-[dangrek] pt-3 text-2xl">Password</Text>
          <TextInput
            ref={passwordInputRef}
            className={`font-[dangrek] text-2xl bg-white rounded-2xl w-60 h-16 pt-2 pl-4 ${editMode.password ? 'text-black' : 'text-stone-500'}`}
            name="password"
            placeholder="********"
            placeholderTextColor="rgba(0,0,0,0.5)"
            returnKeyType="go"
            secureTextEntry
            value={password}
            editable={editMode.password}
            onChangeText={setPassword}
          />
          <TouchableOpacity
            onPress={() => editMode.password ? handleUpdate('password') : handleEditToggle('password')}
            className="justify-center items-center bg-white rounded-r-2xl w-16 h-16 ml-[-65px]"
          >
            <PencilSquareIcon size={23} stroke={50} color="#000000" />
          </TouchableOpacity>
        </View>
        {errors.password && <Text style={styles.text}>{errors.password}</Text>}
        {showSaveCancel && (
          <View className="flex-row space-x-5 px-10 mb-5">
            <TouchableOpacity onPress={handleCancel} className="bg-white rounded-2xl w-[166px] h-20 justify-center items-center">
              <Text className="font-[dangrek] text-2xl pt-3">Cancel</Text>
            </TouchableOpacity>
            <TouchableOpacity onPress={handleUpdate} className="bg-[#397CE1] rounded-2xl w-[166px] h-20 justify-center items-center">
              <Text className="font-[dangrek] text-white text-2xl pt-3">Save</Text>
            </TouchableOpacity>
          </View>
        )}
        {!editMode.username && !editMode.email && !editMode.password && (
          <View>
            <TouchableOpacity onPress={() => navigation.navigate('Login')} className="bg-[#397CE1] rounded-2xl w-[166px] h-20 justify-center items-center">
              <Text className="font-[dangrek] text-white text-2xl pt-3">Logout</Text>
            </TouchableOpacity>
          </View>
        )}
      </View>
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  text: {
    marginTop: -15,
    marginBottom: 5,
    fontSize: "16",
    fontFamily: "dangrek",
    textAlign: "center",
    color: "red",
  },
});

AppRegistry.registerComponent("User", () => User);