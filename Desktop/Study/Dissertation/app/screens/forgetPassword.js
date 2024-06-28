import React, { Component } from "react";
import {
  AppRegistry,
  StyleSheet,
  SafeAreaView,
  Text,
  View,
  Button,
  TextInput,
  TouchableOpacity,
  KeyboardAvoidingView
} from "react-native";
import { ChevronLeftIcon } from 'react-native-heroicons/solid';

export default class ForgetPassword extends Component {
  constructor() {
    super();
    this.state = {
      email: "",
      password: "",
    };
  }
  static navigationOptions = {
    headerStyle: {
      backgroundColor: "#16a085",
      elevation: null
    }
  };

  onForgetPress() {
        this.props.navigation.navigate("Login");
  }
  render() {

    const { navigation } = this.props;

    return (
      <SafeAreaView className="flex-1 bg-[#CCE0FF] justify-start p-20 pt-100">
        <View className="flex-row justify-between mx-4 items-center">
            <TouchableOpacity onPress={()=> navigation.goBack()} className="bg-white rounded-full p-3 shadow">
                <ChevronLeftIcon size="23" stroke={50} color="#434343" />
            </TouchableOpacity>
            </View>
        <KeyboardAvoidingView style={styles.keyboard}>
        <TextInput
          style={styles.input}
          placeholder="Username"
          placeholderTextColor="rgba(0,0,0,0.5)"
          keyboardType="email-address"
          autoCapitalize="none"
          autoCorrect={false}
          value={this.state.email}
          onChangeText={email => this.setState({ email })}
        />
        <TouchableOpacity
          style={styles.buttonContainer}
          onPress={this.onForgetPress.bind(this)}
        >
          <Text style={styles.buttonText}>Forget Password</Text>
        </TouchableOpacity>
        </KeyboardAvoidingView>
      </SafeAreaView>
    );
  }
}

const styles = StyleSheet.create({
  // container: {
  //   flex: 1.2,
  //   justifyContent: "flex-start",
  //   backgroundColor: "#CCE0FF",
  //   padding: 20,
  //   paddingTop: 100
  // },
  keyboard: {
    margin: 20,
    padding: 20,
    alignSelf: "stretch"
  },
  input: {
    fontFamily: "Dangrek",
    fontSize: "25",
    textAlign: "center",
    backgroundColor: "#fff",
    marginBottom: 10,
    borderRadius: 20,
    padding: 15,
    color: "#000000",
  },
  buttonContainer: {
    marginTop: 10,
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
});

AppRegistry.registerComponent("ForgetPassword", () => ForgetPassword);