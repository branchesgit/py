
const fs = require('fs')
function isFileExists(path) {
    try{
        const stat = fs.statSync(path);
        return !!stat
    }catch(e) {
        return false
    }
}

function getFileStat(path) {
    const stat = fs.statSync(path);
    return stat && stat.ctime
}



function filterFiles() {
    let files = ["D:/study/py/v1/", "D:/study/py/imgs/", "D:/study/py/v2/"];

    files = files.filter((file) => {
        const isExists = isFileExists(file);
        if (isExists) {
            const state = getFileStat(file)
            const dis = +new Date() - state;
            console.log(dis)
    
            return dis > 4 * 60 * 1000;
        }
        return false
    }, [])
    
    console.log('files == ', files)
}


filterFiles();