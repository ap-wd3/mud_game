import React, { useState, useRef } from "react";
import { ChevronLeftIcon } from 'react-native-heroicons/solid';
import CheckBox from "expo-checkbox";
import { Dangrek_400Regular } from "@expo-google-fonts/dangrek";
import { useFonts } from "expo-font";
import {
  AppRegistry,
  SafeAreaView,
  StyleSheet,
  Text,
  View,
  TextInput,
  TouchableHighlight,
  Image,
  KeyboardAvoidingView,
  TouchableOpacity
} from "react-native";
import validation from "../validations/registerValidation"
import axios from 'axios';

export default function Register(props) {
  const navigation = props.navigation;
  // const [toggleCheckBox, setToggleCheckBox] = useState(false);
  const [errors, setErrors] = useState({});
  const emailInputRef = useRef(null);
  const passwordInputRef = useRef(null);
  const passwordConfirmInputRef = useRef(null);
  const [values, setValues] = useState({
    username: '',
    email: '',
    password: '',
    password_confirmation: '',
  });
  let [fontsLoaded] = useFonts({
    Dangrek_400Regular,
  });

  const handleInput = (name, value) => {
    setValues(prev => ({ ...prev, [name]: value }));
  };

  const checkEmailExists = async (email) => {
    try {
      const response = await axios.get('https://exciting-monster-living.ngrok-free.app/getUser', { params: { email } });
      if (response.data && response.data.email) {
        return true; 
      }
      return false; 
    } catch (error) {
      if (error.response && error.response.status === 404) {
        return false;
      }
      console.log("Email check error:", error);
      return false;
    }
  };

  const handleSubmit = async () => {
    setErrors({});
    const err = validation(values);
    setErrors(err);  
    if (err.username === "" && err.email === "" && err.password === "" && err.password_confirmation === "") {
      const emailExists = await checkEmailExists(values.email); // Use await here

      if (emailExists) {
        setErrors({ ...err, email: 'This email has been registered' });
        return;
      }
      
      axios.post('https://exciting-monster-living.ngrok-free.app/signup', values)
      .then(res => {
        navigation.navigate("Login");
      })
      .catch(err => {
        console.log("Axios error:", err);
      });
  }};

  // const handleTermsPress = () => {
  //   // Example: navigation.navigate('TermsConditions');
  //   console.log("Navigate to terms & conditions page");
  // };

  if (!fontsLoaded) {
    return <Text>Text Loading...</Text>;
  }

  return (
    <SafeAreaView className="flex-1 bg-[#CCE0FF] justify-start p-20 pt-100">
      <View className="flex-row justify-between mx-4 items-center">
        <TouchableOpacity onPress={() => navigation.goBack()} className="bg-white rounded-full p-3 shadow">
          <ChevronLeftIcon size={23} stroke={50} color="#434343" />
        </TouchableOpacity>
      </View>
      <View style={styles.logoContainer}>
        <Image style={styles.logo} source={require("../assets/logo.png")} />
        <Text style={styles.subtext}>Sign Up</Text>
      </View>
      <KeyboardAvoidingView style={styles.keyboard} behavior="padding">
      <TextInput
          name="username"
          value={values.username}
          onChangeText={(text) => handleInput('username', text)}
          style={styles.input}
          placeholder="Name"
          placeholderTextColor="rgba(0,0,0,0.5)"
          returnKeyType="next"
          onSubmitEditing={() => emailInputRef.current.focus()}
        />
        {errors.username && <Text style={styles.text}>{errors.username}</Text>}
        <TextInput
          name="email"
          value={values.email}
          onChangeText={(text) => handleInput('email', text)}
          style={styles.input}
          placeholder="Email"
          placeholderTextColor="rgba(0,0,0,0.5)"
          returnKeyType="next"
          ref={emailInputRef}
          onSubmitEditing={() => passwordInputRef.current.focus()}
          keyboardType="email-address"
          autoCapitalize="none"
          autoCorrect={false}
        />
        {errors.email && <Text style={styles.text}>{errors.email}</Text>}
        <TextInput
          name="password"
          value={values.password}
          onChangeText={(text) => handleInput('password', text)}
          style={styles.input}
          placeholder="Password"
          secureTextEntry={true}
          placeholderTextColor="rgba(0,0,0,0.5)"
          ref={passwordInputRef}
          onSubmitEditing={() => passwordConfirmInputRef.current.focus()}
          returnKeyType="next"
          textContentType="none"
        />
        {errors.password && <Text style={styles.text}>{errors.password}</Text>}
        <TextInput
          name="password_confirmation"
          value={values.password_confirmation}
          onChangeText={(text) => handleInput('password_confirmation', text)}
          style={styles.input}
          placeholder="Confirm Password"
          secureTextEntry={true}
          placeholderTextColor="rgba(0,0,0,0.5)"
          returnKeyType="go"
          ref={passwordConfirmInputRef}
          textContentType="none"
        />
        {errors.password_confirmation && <Text style={styles.text}>{errors.password_confirmation}</Text>}
        {/* <View className="flex-row mt-2 mb-5 items-center justify-center">
          <CheckBox
            className="mr-3"
            name="checkbox"
            disabled={false}
            value={toggleCheckBox}
            onValueChange={(newValue) => setToggleCheckBox(newValue)}
          />
          <TouchableOpacity onPress={handleTermsPress}>
            <Text className="font-['dangrek'] text-sm underline text-gray-900">Terms & Conditions</Text>
          </TouchableOpacity>
        </View>
        {errors.checkbox && <Text style={styles.text}>{errors.checkbox}</Text>} */}
        <TouchableHighlight
          onPress={handleSubmit}
          style={styles.button}
        >
          <Text style={styles.buttonText}>Register</Text>
        </TouchableHighlight>
      </KeyboardAvoidingView>
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  keyboard: {
    margin: 20,
    padding: 20,
    alignSelf: "stretch"
  },
  logoContainer: {
    alignItems: "center",
    justifyContent: "center",
    alignItems: "center",
    marginBottom: -20
  },
  logo: {
    marginBottom: -30
  },
  subtext: {
    color: "#000000",
    fontFamily: "dangrek",
    fontSize: "60",
    marginTop: 10,
    textAlign: "center"
  },
  input: {
    backgroundColor: "#fff",
    padding: 15,
    borderRadius: 20,
    marginBottom: 15,
    fontFamily: "dangrek",
    fontSize: "25",
    textAlign: "center",
    color: "#000000"
  },  
  text: {
    marginTop: -15,
    marginBottom: 5,
    fontSize: "16",
    fontFamily: "dangrek",
    textAlign: "center",
    color: "red",
  },
  button: {
    backgroundColor: "#000000",
    padding: 15,
    borderRadius: 20,
    marginTop: 10,
    marginBottom: 10,
    alignSelf: "stretch",
    justifyContent: "center"
  },
  buttonText: {
    fontFamily: "dangrek",
    fontSize: "30",
    textAlign: "center",
    color: "#FFF"
  }
});

AppRegistry.registerComponent("Register", () => Register);