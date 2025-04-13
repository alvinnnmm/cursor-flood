import axios from 'axios';

async function testAPI() {
    try {
        const response = await axios.get('https://api.example.com/data');
        console.log('API Response:', response.data);
    } catch (error) {
        console.error('Error calling API:', error);
    }
}

testAPI(); 