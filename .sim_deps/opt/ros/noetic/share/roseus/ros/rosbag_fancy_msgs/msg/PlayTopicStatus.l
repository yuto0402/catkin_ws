;; Auto-generated. Do not edit!


(when (boundp 'rosbag_fancy_msgs::PlayTopicStatus)
  (if (not (find-package "ROSBAG_FANCY_MSGS"))
    (make-package "ROSBAG_FANCY_MSGS"))
  (shadow 'PlayTopicStatus (find-package "ROSBAG_FANCY_MSGS")))
(unless (find-package "ROSBAG_FANCY_MSGS::PLAYTOPICSTATUS")
  (make-package "ROSBAG_FANCY_MSGS::PLAYTOPICSTATUS"))

(in-package "ROS")
;;//! \htmlinclude PlayTopicStatus.msg.html


(defclass rosbag_fancy_msgs::PlayTopicStatus
  :super ros::object
  :slots (_name _rate _bandwidth ))

(defmethod rosbag_fancy_msgs::PlayTopicStatus
  (:init
   (&key
    ((:name __name) "")
    ((:rate __rate) 0.0)
    ((:bandwidth __bandwidth) 0.0)
    )
   (send-super :init)
   (setq _name (string __name))
   (setq _rate (float __rate))
   (setq _bandwidth (float __bandwidth))
   self)
  (:name
   (&optional __name)
   (if __name (setq _name __name)) _name)
  (:rate
   (&optional __rate)
   (if __rate (setq _rate __rate)) _rate)
  (:bandwidth
   (&optional __bandwidth)
   (if __bandwidth (setq _bandwidth __bandwidth)) _bandwidth)
  (:serialization-length
   ()
   (+
    ;; string _name
    4 (length _name)
    ;; float32 _rate
    4
    ;; float32 _bandwidth
    4
    ))
  (:serialize
   (&optional strm)
   (let ((s (if strm strm
              (make-string-output-stream (send self :serialization-length)))))
     ;; string _name
       (write-long (length _name) s) (princ _name s)
     ;; float32 _rate
       (sys::poke _rate (send s :buffer) (send s :count) :float) (incf (stream-count s) 4)
     ;; float32 _bandwidth
       (sys::poke _bandwidth (send s :buffer) (send s :count) :float) (incf (stream-count s) 4)
     ;;
     (if (null strm) (get-output-stream-string s))))
  (:deserialize
   (buf &optional (ptr- 0))
   ;; string _name
     (let (n) (setq n (sys::peek buf ptr- :integer)) (incf ptr- 4) (setq _name (subseq buf ptr- (+ ptr- n))) (incf ptr- n))
   ;; float32 _rate
     (setq _rate (sys::peek buf ptr- :float)) (incf ptr- 4)
   ;; float32 _bandwidth
     (setq _bandwidth (sys::peek buf ptr- :float)) (incf ptr- 4)
   ;;
   self)
  )

(setf (get rosbag_fancy_msgs::PlayTopicStatus :md5sum-) "f9fdaffdd7fc115927db7f4b9e8cca43")
(setf (get rosbag_fancy_msgs::PlayTopicStatus :datatype-) "rosbag_fancy_msgs/PlayTopicStatus")
(setf (get rosbag_fancy_msgs::PlayTopicStatus :definition-)
      "
string name

float32 rate
float32 bandwidth

")



(provide :rosbag_fancy_msgs/PlayTopicStatus "f9fdaffdd7fc115927db7f4b9e8cca43")


