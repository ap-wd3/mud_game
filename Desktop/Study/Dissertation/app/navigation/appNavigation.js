import React from 'react'
import { NavigationContainer } from '@react-navigation/native';
import { createNativeStackNavigator } from '@react-navigation/native-stack';
import { LogBox } from 'react-native';
import Login from '../screens/login';
import Register from '../screens/register';
import ForgetPassword from '../screens/forgetPassword';
import TopicSelect from '../screens/topicSelect';
import Flashcard from '../screens/flashcard';
import Game from '../screens/game';
import Leaderboard from '../screens/leaderboard';
import User from '../screens/user';
import PicSetting from '../screens/picSetting';
import SetSelect from '../screens/setSelect';
import WordDict from '../screens/wordDict';

const Stack = createNativeStackNavigator();

LogBox.ignoreLogs([
  'Non-serializable values were found in the navigation state',
]);

export default function AppNavigation() {
  return (
    <NavigationContainer>
      <Stack.Navigator initialRouteName='Login'>
        <Stack.Screen name="Login" options={{headerShown: false}} component={Login} />
        <Stack.Screen name="Register" options={{headerShown: false}} component={Register} />
        <Stack.Screen name="ForgetPassword" options={{headerShown: false}} component={ForgetPassword} />
        <Stack.Screen name="TopicSelect" options={{headerShown: false}} component={TopicSelect} />
        <Stack.Screen name="SetSelect" options={{headerShown: false}} component={SetSelect} />
        <Stack.Screen name="Flashcard" options={{headerShown: false}} component={Flashcard} />
        <Stack.Screen name="Game" options={{headerShown: false}} component={Game} />
        <Stack.Screen name="Leaderboard" options={{headerShown: false}} component={Leaderboard} />
        <Stack.Screen name="User" options={{headerShown: false}} component={User} />
        <Stack.Screen name="PicSetting" options={{headerShown: false}} component={PicSetting} />
        <Stack.Screen name="WordDict" options={{headerShown: false}} component={WordDict} />
      </Stack.Navigator>
    </NavigationContainer>
  )
}