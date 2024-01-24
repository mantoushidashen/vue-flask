import request from '@/utils/request'

export function uploadFile(data) {
  return request({
    url: 'api/upload',
    method: 'post',
    data
  })
}

export function getFile(filename) {
  return request({
    url: 'download/' + filename + '.xlsx',
    method: 'get',
  })
}
