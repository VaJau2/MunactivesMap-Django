import axios from 'axios'

export const HTTP = axios.create({
    // baseURL: 'http://localhost:8000/api/munactives'
    baseURL: 'http://vaja72.pythonanywhere.com/api/munactives'
})
