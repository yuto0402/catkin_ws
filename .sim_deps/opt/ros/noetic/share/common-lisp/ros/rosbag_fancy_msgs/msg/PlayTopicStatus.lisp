; Auto-generated. Do not edit!


(cl:in-package rosbag_fancy_msgs-msg)


;//! \htmlinclude PlayTopicStatus.msg.html

(cl:defclass <PlayTopicStatus> (roslisp-msg-protocol:ros-message)
  ((name
    :reader name
    :initarg :name
    :type cl:string
    :initform "")
   (rate
    :reader rate
    :initarg :rate
    :type cl:float
    :initform 0.0)
   (bandwidth
    :reader bandwidth
    :initarg :bandwidth
    :type cl:float
    :initform 0.0))
)

(cl:defclass PlayTopicStatus (<PlayTopicStatus>)
  ())

(cl:defmethod cl:initialize-instance :after ((m <PlayTopicStatus>) cl:&rest args)
  (cl:declare (cl:ignorable args))
  (cl:unless (cl:typep m 'PlayTopicStatus)
    (roslisp-msg-protocol:msg-deprecation-warning "using old message class name rosbag_fancy_msgs-msg:<PlayTopicStatus> is deprecated: use rosbag_fancy_msgs-msg:PlayTopicStatus instead.")))

(cl:ensure-generic-function 'name-val :lambda-list '(m))
(cl:defmethod name-val ((m <PlayTopicStatus>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader rosbag_fancy_msgs-msg:name-val is deprecated.  Use rosbag_fancy_msgs-msg:name instead.")
  (name m))

(cl:ensure-generic-function 'rate-val :lambda-list '(m))
(cl:defmethod rate-val ((m <PlayTopicStatus>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader rosbag_fancy_msgs-msg:rate-val is deprecated.  Use rosbag_fancy_msgs-msg:rate instead.")
  (rate m))

(cl:ensure-generic-function 'bandwidth-val :lambda-list '(m))
(cl:defmethod bandwidth-val ((m <PlayTopicStatus>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader rosbag_fancy_msgs-msg:bandwidth-val is deprecated.  Use rosbag_fancy_msgs-msg:bandwidth instead.")
  (bandwidth m))
(cl:defmethod roslisp-msg-protocol:serialize ((msg <PlayTopicStatus>) ostream)
  "Serializes a message object of type '<PlayTopicStatus>"
  (cl:let ((__ros_str_len (cl:length (cl:slot-value msg 'name))))
    (cl:write-byte (cl:ldb (cl:byte 8 0) __ros_str_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) __ros_str_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) __ros_str_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) __ros_str_len) ostream))
  (cl:map cl:nil #'(cl:lambda (c) (cl:write-byte (cl:char-code c) ostream)) (cl:slot-value msg 'name))
  (cl:let ((bits (roslisp-utils:encode-single-float-bits (cl:slot-value msg 'rate))))
    (cl:write-byte (cl:ldb (cl:byte 8 0) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) bits) ostream))
  (cl:let ((bits (roslisp-utils:encode-single-float-bits (cl:slot-value msg 'bandwidth))))
    (cl:write-byte (cl:ldb (cl:byte 8 0) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) bits) ostream))
)
(cl:defmethod roslisp-msg-protocol:deserialize ((msg <PlayTopicStatus>) istream)
  "Deserializes a message object of type '<PlayTopicStatus>"
    (cl:let ((__ros_str_len 0))
      (cl:setf (cl:ldb (cl:byte 8 0) __ros_str_len) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) __ros_str_len) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 16) __ros_str_len) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 24) __ros_str_len) (cl:read-byte istream))
      (cl:setf (cl:slot-value msg 'name) (cl:make-string __ros_str_len))
      (cl:dotimes (__ros_str_idx __ros_str_len msg)
        (cl:setf (cl:char (cl:slot-value msg 'name) __ros_str_idx) (cl:code-char (cl:read-byte istream)))))
    (cl:let ((bits 0))
      (cl:setf (cl:ldb (cl:byte 8 0) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 16) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 24) bits) (cl:read-byte istream))
    (cl:setf (cl:slot-value msg 'rate) (roslisp-utils:decode-single-float-bits bits)))
    (cl:let ((bits 0))
      (cl:setf (cl:ldb (cl:byte 8 0) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 16) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 24) bits) (cl:read-byte istream))
    (cl:setf (cl:slot-value msg 'bandwidth) (roslisp-utils:decode-single-float-bits bits)))
  msg
)
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql '<PlayTopicStatus>)))
  "Returns string type for a message object of type '<PlayTopicStatus>"
  "rosbag_fancy_msgs/PlayTopicStatus")
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql 'PlayTopicStatus)))
  "Returns string type for a message object of type 'PlayTopicStatus"
  "rosbag_fancy_msgs/PlayTopicStatus")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql '<PlayTopicStatus>)))
  "Returns md5sum for a message object of type '<PlayTopicStatus>"
  "f9fdaffdd7fc115927db7f4b9e8cca43")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql 'PlayTopicStatus)))
  "Returns md5sum for a message object of type 'PlayTopicStatus"
  "f9fdaffdd7fc115927db7f4b9e8cca43")
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql '<PlayTopicStatus>)))
  "Returns full string definition for message of type '<PlayTopicStatus>"
  (cl:format cl:nil "~%string name~%~%float32 rate~%float32 bandwidth~%~%~%"))
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql 'PlayTopicStatus)))
  "Returns full string definition for message of type 'PlayTopicStatus"
  (cl:format cl:nil "~%string name~%~%float32 rate~%float32 bandwidth~%~%~%"))
(cl:defmethod roslisp-msg-protocol:serialization-length ((msg <PlayTopicStatus>))
  (cl:+ 0
     4 (cl:length (cl:slot-value msg 'name))
     4
     4
))
(cl:defmethod roslisp-msg-protocol:ros-message-to-list ((msg <PlayTopicStatus>))
  "Converts a ROS message object to a list"
  (cl:list 'PlayTopicStatus
    (cl:cons ':name (name msg))
    (cl:cons ':rate (rate msg))
    (cl:cons ':bandwidth (bandwidth msg))
))
