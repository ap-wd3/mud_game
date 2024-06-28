import React, { useState } from "react";
import {
  AppRegistry,
  SafeAreaView,
  KeyboardAvoidingView,
  TouchableOpacity,
  Image,
  TextInput,
  StyleSheet,
  Text,
  View,
} from "react-native";
import AsyncStorage from "@react-native-async-storage/async-storage";
import { Dangrek_400Regular } from "@expo-google-fonts/dangrek";
import { useFonts } from "expo-font";
import validation from "../validations/loginValidation";
import axios from 'axios';
import { useFocusEffect } from '@react-navigation/native';


export default function Login(props) {
  const navigation = props.navigation;
  const [values, setValues] = useState({
    email: '',
    password: ''
  });
  const [errors, setErrors] = useState({});

  const handleInput = (name, value) => {
    setValues(prev => ({ ...prev, [name]: value }));
  };

  const handleSubmit = (event) => {
    const err = validation(values);
    setErrors(err);
    if(err.email === "" && err.password === "") {
      axios.post('https://exciting-monster-living.ngrok-free.app/login', values) // ngrok
      .then(async (res) => {
        if(res.data.status === "Success") {
          console.log('data', res.data)
          await AsyncStorage.setItem('username', res.data.username);  // Store the username
          await AsyncStorage.setItem('user_id', res.data.user_id.toString());
          await AsyncStorage.setItem('email', res.data.email);
          await AsyncStorage.setItem('img', res.data.img);
          await AsyncStorage.setItem('type', res.data.type);
          navigation.navigate("TopicSelect", { 
            user_id: res.data.user_id,
            username: res.data.username,
            email: res.data.email,
            password: res.data.password,
            img: res.data.img,
            type: res.data.type,
          });
        } else {
          setErrors(prev => ({ ...prev, login: "Your email or password is wrong" }));
        }
      })
      .catch(err => {
        console.log("Axios error:", err);
      });
    }
  };

  useFocusEffect(
    React.useCallback(() => {
      setErrors({});
      setValues({});
    }, [])
  );

  const [fontsLoaded] = useFonts({
    Dangrek_400Regular,
  });

  if (!fontsLoaded) {
    return <Text>Font Loading...</Text>;
  }
  return (
    <SafeAreaView style={styles.container}>
      <View behavior="padding" style={styles.logoContainer}>
        <Image style={styles.logo} source={require("../assets/logo.png")} />
        <Text style={styles.subtext}>Login</Text>
      </View>
      <KeyboardAvoidingView style={styles.keyboard}>
        <View style={styles.window}>
          <TextInput
            name="email"
            style={styles.inputText}
            placeholder="Email Address"
            placeholderTextColor="rgba(0,0,0,0.5)"
            returnKeyType="next"
            onSubmitEditing={() => this.passwordInput.focus()}
            keyboardType="email-address"
            autoCapitalize="none"
            autoCorrect={false}
            value={values.email}
            onChangeText={(text) => handleInput('email', text)}
            />
        </View>
        {errors.email && <Text style={styles.text}>{errors.email}</Text>}
        <View style={styles.window}>
          <TextInput
            name="password"
            style={styles.inputText}
            placeholder="Password"
            placeholderTextColor="rgba(0,0,0,0.5)"
            returnKeyType="go"
            secureTextEntry
            ref={(input) => (this.passwordInput = input)}
            value={values.password}
            onChangeText={(text) => handleInput('password', text)}
          />
        </View>
        {errors.password && <Text style={styles.text}>{errors.password}</Text>}
        {errors.login && <Text style={styles.text}>{errors.login}</Text>}
        <TouchableOpacity style={styles.loginContainer} onPress={handleSubmit}>
          <Text style={styles.buttonText}>Login</Text>
        </TouchableOpacity>

        <TouchableOpacity style={styles.forgetButton}>
          <Text
            style={styles.forgetText}
            onPress={() => navigation.navigate("ForgetPassword")}
          >
            Forget Password
          </Text>
        </TouchableOpacity>

        <TouchableOpacity style={styles.signupContainer}>
          <Text
            style={styles.buttonText}
            onPress={() => navigation.navigate("Register")}
          >
            Sign up
          </Text>
        </TouchableOpacity>
      </KeyboardAvoidingView>
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    justifyContent: "center",
    backgroundColor: "#CCE0FF",
    alignItems: "center"
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
    fontFamily: "Dangrek",
    fontSize: "60",
    marginTop: 10,
    width: 160,
    textAlign: "center"
  },
  keyboard: {
    margin: 20,
    padding: 20,
    alignSelf: "stretch"
  },
  loginContainer: {
    backgroundColor: "#000000",
    padding: 15,
    borderRadius: 20,
    marginBottom: -5
  },
  buttonText: {
    fontFamily: "Dangrek",
    fontSize: "30",
    textAlign: "center",
    color: "#FFF"
  },
  signupContainer: {
    backgroundColor: "#397CE1",
    padding: 15,
    borderRadius: 20
  },
  forgetButton: {
    paddingVertical: 15,
    marginBottom: 10
  },
  forgetText: {
    fontSize: "20",
    fontFamily: "Dangrek",
    textAlign: "center"
  },
  window: {
    backgroundColor: "#fff",
    padding: 15,
    borderRadius: 20,
    marginBottom: 15
  },
  inputText: {
    fontFamily: "Dangrek",
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
  }
});

AppRegistry.registerComponent("Login", () => Login);