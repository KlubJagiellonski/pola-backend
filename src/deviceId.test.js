import React from "react";
import {getCurrentDeviceId} from "./deviceId";

beforeEach(() => localStorage.removeItem('DEVICE_ID', 'WEB-FAKE-ID'))


test('return random ID', () => {
    expect(getCurrentDeviceId()).toHaveLength(32 + 4)
});

test('should save device ID', () => {
    const a = getCurrentDeviceId()
    const b = getCurrentDeviceId()
    expect(a).toEqual(b)
    expect(typeof localStorage.getItem('DEVICE_ID')).toEqual('string')
});

