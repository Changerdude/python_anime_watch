// function get_animes(){
//     fetch("https://kitsu.io/api/edge/anime?filter[status]=current&filter[subtype]=TV")
//         .then(response => response.json() )
//         .then(data => {
//         console.log(data)
//         let result = [];
//         for(let incAnime in data.data.attributes){
//             console.log(incAnime);
//             let anime ={
//                 "title" : incAnime.canonicalTitle,
//                 "description" : incAnime.description,
//                 "image" : incAnime.posterImage.large
//             }
//             result.push(anime)
//         }
        
//     })
//     .catch(err => console.log(err) )
// }
// var animes = get_animes();