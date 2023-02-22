(defun get-file (filename)
  (mapcar #'parse-integer
    (with-open-file (stream filename)
      (loop for line = (read-line stream nil)
            while line
            collect line))))

(defun prod-when-sum-of-two-is-2020 (numbers)
  (loop for number-1 in numbers
        do (loop for number-2 in numbers
                 when (= 2020 (+ number-1 number-2))
                 do (return (* number-1 number-2)))))

(defun prod-when-sum-of-three-is-2020 (numbers)
  (loop for number-1 in numbers
        do (loop for number-2 in numbers
            do (loop for number-3 in numbers
                     when (= 2020 (+ number-1 number-2 number-3))
                     do (return (* number-1 number-2 number-3))))))

(let ((numbers (sort (get-file "inputs/1") #'<)))
    (format t "~A~%" (prod-when-sum-of-two-is-2020 numbers))
    (format t "~A~%" (prod-when-sum-of-three-is-2020 numbers)))
