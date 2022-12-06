(defun get-file (filename)
  (mapcar #'parse-integer
    (with-open-file (stream filename)
      (loop for line = (read-line stream nil)
            while line
            collect line))))
(let ((numbers (get-file "inputs/1")))
  (loop for number-1 in numbers
        do (loop for number-2 in numbers
                 do (if (equalp 2020 (+ number-1 number-2))
                      (format t "~A~%" (* number-1 number-2)))))
  (loop for number-1 in numbers
        do (loop for number-2 in numbers
                 do (loop for number-3 in numbers
                          do (if (equalp 2020 (+ number-1 number-2 number-3))
                               (format t "~A~%" (* number-1 number-2 number-3)))))))
