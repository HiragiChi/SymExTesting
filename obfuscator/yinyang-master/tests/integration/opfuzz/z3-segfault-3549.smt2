; Bug hidden by distinct -> = 
(set-option :trace true)
(declare-fun a () (_ FloatingPoint 11 53))
(declare-fun b () (_ FloatingPoint 8 24))
(assert (= b ((_ to_fp 8 24) RTP a)))
(check-sat)
