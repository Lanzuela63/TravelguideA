import React, { useState, useContext, FC } from 'react'
import { View, StyleSheet, Text, ScrollView, Alert } from 'react-native'
import { TextInput, Button, Card, Title, IconButton } from 'react-native-paper'
import { Picker } from '@react-native-picker/picker'
import { useNavigation } from '@react-navigation/native'
import { AuthContext } from '../context/AuthContext'
import { AuthStackParamList } from '../navigation/AuthNavigator' // Import AuthStackParamList

const RegisterScreen: FC = () => {
  const navigation = useNavigation<any>(); // Cast to any for now
  const { register } = useContext(AuthContext);

  const [username, setUsername] = useState<string>('')
  const [email, setEmail] = useState<string>('')
  const [password, setPassword] = useState<string>('')
  const [role, setRole] = useState<string>('Tourist') // default

  const onRegisterPress = () => {
    if (!username || !email || !password || !role) {
      Alert.alert('Validation Error', 'Please fill in all fields.')
      return
    }
    register({ username, email, password, role, navigation })
  }

  return (
    <ScrollView contentContainerStyle={styles.container}>
      <Card style={styles.card}>
        <Card.Content>
          <View style={styles.header}>
            <IconButton icon='arrow-left' onPress={() => navigation.goBack()} />
            <Title style={styles.title}>Create an Account</Title>
          </View>

          <TextInput
            label='Username'
            value={username}
            onChangeText={setUsername}
            mode='outlined'
            style={styles.input}
          />

          <TextInput
            label='Email'
            value={email}
            onChangeText={setEmail}
            mode='outlined'
            keyboardType='email-address'
            autoCapitalize='none'
            style={styles.input}
          />

          <TextInput
            label='Password'
            value={password}
            onChangeText={setPassword}
            secureTextEntry
            mode='outlined'
            style={styles.input}
          />

          <Text style={styles.roleLabel}>Select Role</Text>
          <View style={styles.pickerWrapper}>
            <Picker
              selectedValue={role}
              onValueChange={(itemValue: string) => setRole(itemValue)} // Explicitly type itemValue
            >
              <Picker.Item label='Tourist' value='Tourist' />
              <Picker.Item label='Tourism Officer' value='Tourism Officer' />
              <Picker.Item label='Business Owner' value='Business Owner' />
              <Picker.Item label='Event Organizer' value='Event Organizer' />
            </Picker>
          </View>

          <Button
            mode='contained'
            onPress={onRegisterPress}
            style={styles.registerButton}
          >
            Register
          </Button>
        </Card.Content>
      </Card>
    </ScrollView>
  )
}

export default RegisterScreen

const styles = StyleSheet.create({
  container: {
    flexGrow: 1,
    justifyContent: 'center',
    padding: 20,
    backgroundColor: '#f0f4f8'
  },
  card: {
    padding: 10,
    borderRadius: 12,
    elevation: 4
  },
  header: {
    flexDirection: 'row',
    alignItems: 'center',
    marginBottom: 16
  },
  title: {
    fontSize: 22,
    fontWeight: 'bold',
    marginLeft: 8
  },
  input: {
    marginBottom: 12
  },
  roleLabel: {
    marginTop: 16,
    marginBottom: 4
  },
  pickerWrapper: {
    borderWidth: 1,
    borderColor: '#ccc',
    borderRadius: 5,
    overflow: 'hidden',
    marginBottom: 12
  },
  registerButton: {
    marginTop: 24
  }
})