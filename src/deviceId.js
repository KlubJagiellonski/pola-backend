export const randomString = (len) => {
    let result = ""
    for (let i = 0; i < len; i++) {
        let asciiNumber = Math.floor(Math.random() * 35);
        if (asciiNumber >= 0 && asciiNumber <= 9) {
            result = result + String.fromCharCode(asciiNumber + 48)
        } else {
            result = result + String.fromCharCode(asciiNumber + 87)
        }
    }
    return result
}

export const randomDeviceId = () => {
    return `WEB-${randomString(32)}`
}

export const getCurrentDeviceId = () => {
    let deviceId = localStorage.getItem('DEVICE_ID')
    if (deviceId == null) {
        deviceId= randomDeviceId()
        localStorage.setItem('DEVICE_ID', deviceId);
    }
    return deviceId;
}