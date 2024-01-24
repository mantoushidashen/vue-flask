import request from '@/utils/request'

export function getNovelChapters(){
    return request({
        url: 'api/novel/chapters',
        method: 'get'
    })
}

export function getNovelChapterContent(chapterUrl){
    return request({
        url: 'api/novel/content/' + chapterUrl,
        method: 'get',
    })
}