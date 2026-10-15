;; Auto-generated. Do not edit!


(when (boundp 'rosbag_fancy_msgs::PlayStatus)
  (if (not (find-package "ROSBAG_FANCY_MSGS"))
    (make-package "ROSBAG_FANCY_MSGS"))
  (shadow 'PlayStatus (find-package "ROSBAG_FANCY_MSGS")))
(unless (find-package "ROSBAG_FANCY_MSGS::PLAYSTATUS")
  (make-package "ROSBAG_FANCY_MSGS::PLAYSTATUS"))

(in-package "ROS")
;;//! \htmlinclude PlayStatus.msg.html
(if (not (find-package "STD_MSGS"))
  (ros::roseus-add-msgs "std_msgs"))


(intern "*STATUS_PAUSED*" (find-package "ROSBAG_FANCY_MSGS::PLAYSTATUS"))
(shadow '*STATUS_PAUSED* (find-package "ROSBAG_FANCY_MSGS::PLAYSTATUS"))
(defconstant rosbag_fancy_msgs::PlayStatus::*STATUS_PAUSED* 0)
(intern "*STATUS_RUNNING*" (find-package "ROSBAG_FANCY_MSGS::PLAYSTATUS"))
(shadow '*STATUS_RUNNING* (find-package "ROSBAG_FANCY_MSGS::PLAYSTATUS"))
(defconstant rosbag_fancy_msgs::PlayStatus::*STATUS_RUNNING* 1)

(defun rosbag_fancy_msgs::PlayStatus-to-symbol (const)
  (cond
        ((= const 0) 'rosbag_fancy_msgs::PlayStatus::*STATUS_PAUSED*)
        ((= const 1) 'rosbag_fancy_msgs::PlayStatus::*STATUS_RUNNING*)
        (t nil)))

(defclass rosbag_fancy_msgs::PlayStatus
  :super ros::object
  :slots (_header _status _duration _current _currentTime _startTime _endTime _bagfiles _topics ))

(defmethod rosbag_fancy_msgs::PlayStatus
  (:init
   (&key
    ((:header __header) (instance std_msgs::Header :init))
    ((:status __status) 0)
    ((:duration __duration) (instance ros::time :init))
    ((:current __current) (instance ros::time :init))
    ((:currentTime __currentTime) (instance ros::time :init))
    ((:startTime __startTime) (instance ros::time :init))
    ((:endTime __endTime) (instance ros::time :init))
    ((:bagfiles __bagfiles) (let (r) (dotimes (i 0) (push "" r)) r))
    ((:topics __topics) ())
    )
   (send-super :init)
   (setq _header __header)
   (setq _status (round __status))
   (setq _duration __duration)
   (setq _current __current)
   (setq _currentTime __currentTime)
   (setq _startTime __startTime)
   (setq _endTime __endTime)
   (setq _bagfiles __bagfiles)
   (setq _topics __topics)
   self)
  (:header
   (&rest __header)
   (if (keywordp (car __header))
       (send* _header __header)
     (progn
       (if __header (setq _header (car __header)))
       _header)))
  (:status
   (&optional __status)
   (if __status (setq _status __status)) _status)
  (:duration
   (&optional __duration)
   (if __duration (setq _duration __duration)) _duration)
  (:current
   (&optional __current)
   (if __current (setq _current __current)) _current)
  (:currentTime
   (&optional __currentTime)
   (if __currentTime (setq _currentTime __currentTime)) _currentTime)
  (:startTime
   (&optional __startTime)
   (if __startTime (setq _startTime __startTime)) _startTime)
  (:endTime
   (&optional __endTime)
   (if __endTime (setq _endTime __endTime)) _endTime)
  (:bagfiles
   (&optional __bagfiles)
   (if __bagfiles (setq _bagfiles __bagfiles)) _bagfiles)
  (:topics
   (&rest __topics)
   (if (keywordp (car __topics))
       (send* _topics __topics)
     (progn
       (if __topics (setq _topics (car __topics)))
       _topics)))
  (:serialization-length
   ()
   (+
    ;; std_msgs/Header _header
    (send _header :serialization-length)
    ;; uint8 _status
    1
    ;; duration _duration
    8
    ;; duration _current
    8
    ;; time _currentTime
    8
    ;; time _startTime
    8
    ;; time _endTime
    8
    ;; string[] _bagfiles
    (apply #'+ (mapcar #'(lambda (x) (+ 4 (length x))) _bagfiles)) 4
    ;; rosbag_fancy_msgs/PlayTopicStatus[] _topics
    (apply #'+ (send-all _topics :serialization-length)) 4
    ))
  (:serialize
   (&optional strm)
   (let ((s (if strm strm
              (make-string-output-stream (send self :serialization-length)))))
     ;; std_msgs/Header _header
       (send _header :serialize s)
     ;; uint8 _status
       (write-byte _status s)
     ;; duration _duration
       (write-long (send _duration :sec) s) (write-long (send _duration :nsec) s)
     ;; duration _current
       (write-long (send _current :sec) s) (write-long (send _current :nsec) s)
     ;; time _currentTime
       (write-long (send _currentTime :sec) s) (write-long (send _currentTime :nsec) s)
     ;; time _startTime
       (write-long (send _startTime :sec) s) (write-long (send _startTime :nsec) s)
     ;; time _endTime
       (write-long (send _endTime :sec) s) (write-long (send _endTime :nsec) s)
     ;; string[] _bagfiles
     (write-long (length _bagfiles) s)
     (dolist (elem _bagfiles)
       (write-long (length elem) s) (princ elem s)
       )
     ;; rosbag_fancy_msgs/PlayTopicStatus[] _topics
     (write-long (length _topics) s)
     (dolist (elem _topics)
       (send elem :serialize s)
       )
     ;;
     (if (null strm) (get-output-stream-string s))))
  (:deserialize
   (buf &optional (ptr- 0))
   ;; std_msgs/Header _header
     (send _header :deserialize buf ptr-) (incf ptr- (send _header :serialization-length))
   ;; uint8 _status
     (setq _status (sys::peek buf ptr- :char)) (incf ptr- 1)
   ;; duration _duration
     (send _duration :sec (sys::peek buf ptr- :integer)) (incf ptr- 4)  (send _duration :nsec (sys::peek buf ptr- :integer)) (incf ptr- 4)
   ;; duration _current
     (send _current :sec (sys::peek buf ptr- :integer)) (incf ptr- 4)  (send _current :nsec (sys::peek buf ptr- :integer)) (incf ptr- 4)
   ;; time _currentTime
     (send _currentTime :sec (sys::peek buf ptr- :integer)) (incf ptr- 4)  (send _currentTime :nsec (sys::peek buf ptr- :integer)) (incf ptr- 4)
   ;; time _startTime
     (send _startTime :sec (sys::peek buf ptr- :integer)) (incf ptr- 4)  (send _startTime :nsec (sys::peek buf ptr- :integer)) (incf ptr- 4)
   ;; time _endTime
     (send _endTime :sec (sys::peek buf ptr- :integer)) (incf ptr- 4)  (send _endTime :nsec (sys::peek buf ptr- :integer)) (incf ptr- 4)
   ;; string[] _bagfiles
   (let (n)
     (setq n (sys::peek buf ptr- :integer)) (incf ptr- 4)
     (setq _bagfiles (make-list n))
     (dotimes (i n)
     (let (n) (setq n (sys::peek buf ptr- :integer)) (incf ptr- 4) (setf (elt _bagfiles i) (subseq buf ptr- (+ ptr- n))) (incf ptr- n))
     ))
   ;; rosbag_fancy_msgs/PlayTopicStatus[] _topics
   (let (n)
     (setq n (sys::peek buf ptr- :integer)) (incf ptr- 4)
     (setq _topics (let (r) (dotimes (i n) (push (instance rosbag_fancy_msgs::PlayTopicStatus :init) r)) r))
     (dolist (elem- _topics)
     (send elem- :deserialize buf ptr-) (incf ptr- (send elem- :serialization-length))
     ))
   ;;
   self)
  )

(setf (get rosbag_fancy_msgs::PlayStatus :md5sum-) "18d8189d68cad8bcb9b6fe0e4a2348ef")
(setf (get rosbag_fancy_msgs::PlayStatus :datatype-) "rosbag_fancy_msgs/PlayStatus")
(setf (get rosbag_fancy_msgs::PlayStatus :definition-)
      "
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

")



(provide :rosbag_fancy_msgs/PlayStatus "18d8189d68cad8bcb9b6fe0e4a2348ef")


