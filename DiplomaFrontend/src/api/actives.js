import { HTTP } from './common'

export const Active = {
    create (active_name, config) {
        return HTTP.post('/' + active_name + '/', config).then(response => {
            return response.data
        })
    },
    delete(active, id) {
        return HTTP.delete('/' + active + '/' + id)
    },
    get (active_name) {
        return HTTP.get('/' + active_name + '/').then(response => {
            return response.data
        })
    },
    update(active_name, active_id, options) {
        return HTTP.patch('/' + active_name + '/' + active_id + '/', options).then(response => {
            return response.data
        })
    }
}