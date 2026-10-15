// Auto-generated. Do not edit!

// (in-package rosbag_fancy_msgs.msg)


"use strict";

const _serializer = _ros_msg_utils.Serialize;
const _arraySerializer = _serializer.Array;
const _deserializer = _ros_msg_utils.Deserialize;
const _arrayDeserializer = _deserializer.Array;
const _finder = _ros_msg_utils.Find;
const _getByteLength = _ros_msg_utils.getByteLength;
let PlayTopicStatus = require('./PlayTopicStatus.js');
let std_msgs = _finder('std_msgs');

//-----------------------------------------------------------

class PlayStatus {
  constructor(initObj={}) {
    if (initObj === null) {
      // initObj === null is a special case for deserialization where we don't initialize fields
      this.header = null;
      this.status = null;
      this.duration = null;
      this.current = null;
      this.currentTime = null;
      this.startTime = null;
      this.endTime = null;
      this.bagfiles = null;
      this.topics = null;
    }
    else {
      if (initObj.hasOwnProperty('header')) {
        this.header = initObj.header
      }
      else {
        this.header = new std_msgs.msg.Header();
      }
      if (initObj.hasOwnProperty('status')) {
        this.status = initObj.status
      }
      else {
        this.status = 0;
      }
      if (initObj.hasOwnProperty('duration')) {
        this.duration = initObj.duration
      }
      else {
        this.duration = {secs: 0, nsecs: 0};
      }
      if (initObj.hasOwnProperty('current')) {
        this.current = initObj.current
      }
      else {
        this.current = {secs: 0, nsecs: 0};
      }
      if (initObj.hasOwnProperty('currentTime')) {
        this.currentTime = initObj.currentTime
      }
      else {
        this.currentTime = {secs: 0, nsecs: 0};
      }
      if (initObj.hasOwnProperty('startTime')) {
        this.startTime = initObj.startTime
      }
      else {
        this.startTime = {secs: 0, nsecs: 0};
      }
      if (initObj.hasOwnProperty('endTime')) {
        this.endTime = initObj.endTime
      }
      else {
        this.endTime = {secs: 0, nsecs: 0};
      }
      if (initObj.hasOwnProperty('bagfiles')) {
        this.bagfiles = initObj.bagfiles
      }
      else {
        this.bagfiles = [];
      }
      if (initObj.hasOwnProperty('topics')) {
        this.topics = initObj.topics
      }
      else {
        this.topics = [];
      }
    }
  }

  static serialize(obj, buffer, bufferOffset) {
    // Serializes a message object of type PlayStatus
    // Serialize message field [header]
    bufferOffset = std_msgs.msg.Header.serialize(obj.header, buffer, bufferOffset);
    // Serialize message field [status]
    bufferOffset = _serializer.uint8(obj.status, buffer, bufferOffset);
    // Serialize message field [duration]
    bufferOffset = _serializer.duration(obj.duration, buffer, bufferOffset);
    // Serialize message field [current]
    bufferOffset = _serializer.duration(obj.current, buffer, bufferOffset);
    // Serialize message field [currentTime]
    bufferOffset = _serializer.time(obj.currentTime, buffer, bufferOffset);
    // Serialize message field [startTime]
    bufferOffset = _serializer.time(obj.startTime, buffer, bufferOffset);
    // Serialize message field [endTime]
    bufferOffset = _serializer.time(obj.endTime, buffer, bufferOffset);
    // Serialize message field [bagfiles]
    bufferOffset = _arraySerializer.string(obj.bagfiles, buffer, bufferOffset, null);
    // Serialize message field [topics]
    // Serialize the length for message field [topics]
    bufferOffset = _serializer.uint32(obj.topics.length, buffer, bufferOffset);
    obj.topics.forEach((val) => {
      bufferOffset = PlayTopicStatus.serialize(val, buffer, bufferOffset);
    });
    return bufferOffset;
  }

  static deserialize(buffer, bufferOffset=[0]) {
    //deserializes a message object of type PlayStatus
    let len;
    let data = new PlayStatus(null);
    // Deserialize message field [header]
    data.header = std_msgs.msg.Header.deserialize(buffer, bufferOffset);
    // Deserialize message field [status]
    data.status = _deserializer.uint8(buffer, bufferOffset);
    // Deserialize message field [duration]
    data.duration = _deserializer.duration(buffer, bufferOffset);
    // Deserialize message field [current]
    data.current = _deserializer.duration(buffer, bufferOffset);
    // Deserialize message field [currentTime]
    data.currentTime = _deserializer.time(buffer, bufferOffset);
    // Deserialize message field [startTime]
    data.startTime = _deserializer.time(buffer, bufferOffset);
    // Deserialize message field [endTime]
    data.endTime = _deserializer.time(buffer, bufferOffset);
    // Deserialize message field [bagfiles]
    data.bagfiles = _arrayDeserializer.string(buffer, bufferOffset, null)
    // Deserialize message field [topics]
    // Deserialize array length for message field [topics]
    len = _deserializer.uint32(buffer, bufferOffset);
    data.topics = new Array(len);
    for (let i = 0; i < len; ++i) {
      data.topics[i] = PlayTopicStatus.deserialize(buffer, bufferOffset)
    }
    return data;
  }

  static getMessageSize(object) {
    let length = 0;
    length += std_msgs.msg.Header.getMessageSize(object.header);
    object.bagfiles.forEach((val) => {
      length += 4 + _getByteLength(val);
    });
    object.topics.forEach((val) => {
      length += PlayTopicStatus.getMessageSize(val);
    });
    return length + 49;
  }

  static datatype() {
    // Returns string type for a message object
    return 'rosbag_fancy_msgs/PlayStatus';
  }

  static md5sum() {
    //Returns md5sum for a message object
    return '18d8189d68cad8bcb9b6fe0e4a2348ef';
  }

  static messageDefinition() {
    // Returns full string definition for message
    return `
    
    uint8 STATUS_PAUSED = 0
    uint8 STATUS_RUNNING = 1
    
    
    Header header
    
    uint8 status
    duration duration
    duration current
    time currentTime
    time startTime
    time endTime
    string[] bagfiles
    
    PlayTopicStatus[] topics
    
    
    ================================================================================
    MSG: std_msgs/Header
    # Standard metadata for higher-level stamped data types.
    # This is generally used to communicate timestamped data 
    # in a particular coordinate frame.
    # 
    # sequence ID: consecutively increasing ID 
    uint32 seq
    #Two-integer timestamp that is expressed as:
    # * stamp.sec: seconds (stamp_secs) since epoch (in Python the variable is called 'secs')
    # * stamp.nsec: nanoseconds since stamp_secs (in Python the variable is called 'nsecs')
    # time-handling sugar is provided by the client library
    time stamp
    #Frame this data is associated with
    string frame_id
    
    ================================================================================
    MSG: rosbag_fancy_msgs/PlayTopicStatus
    
    string name
    
    float32 rate
    float32 bandwidth
    
    `;
  }

  static Resolve(msg) {
    // deep-construct a valid message object instance of whatever was passed in
    if (typeof msg !== 'object' || msg === null) {
      msg = {};
    }
    const resolved = new PlayStatus(null);
    if (msg.header !== undefined) {
      resolved.header = std_msgs.msg.Header.Resolve(msg.header)
    }
    else {
      resolved.header = new std_msgs.msg.Header()
    }

    if (msg.status !== undefined) {
      resolved.status = msg.status;
    }
    else {
      resolved.status = 0
    }

    if (msg.duration !== undefined) {
      resolved.duration = msg.duration;
    }
    else {
      resolved.duration = {secs: 0, nsecs: 0}
    }

    if (msg.current !== undefined) {
      resolved.current = msg.current;
    }
    else {
      resolved.current = {secs: 0, nsecs: 0}
    }

    if (msg.currentTime !== undefined) {
      resolved.currentTime = msg.currentTime;
    }
    else {
      resolved.currentTime = {secs: 0, nsecs: 0}
    }

    if (msg.startTime !== undefined) {
      resolved.startTime = msg.startTime;
    }
    else {
      resolved.startTime = {secs: 0, nsecs: 0}
    }

    if (msg.endTime !== undefined) {
      resolved.endTime = msg.endTime;
    }
    else {
      resolved.endTime = {secs: 0, nsecs: 0}
    }

    if (msg.bagfiles !== undefined) {
      resolved.bagfiles = msg.bagfiles;
    }
    else {
      resolved.bagfiles = []
    }

    if (msg.topics !== undefined) {
      resolved.topics = new Array(msg.topics.length);
      for (let i = 0; i < resolved.topics.length; ++i) {
        resolved.topics[i] = PlayTopicStatus.Resolve(msg.topics[i]);
      }
    }
    else {
      resolved.topics = []
    }

    return resolved;
    }
};

// Constants for message
PlayStatus.Constants = {
  STATUS_PAUSED: 0,
  STATUS_RUNNING: 1,
}

module.exports = PlayStatus;
