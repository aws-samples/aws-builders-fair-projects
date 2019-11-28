
FROM ev3dev/ev3dev-stretch-ev3-generic

COPY ev3dev/controller.py /home/robot/
COPY ev3dev/service.sh /home/robot/
RUN chown robot:robot /home/robot/controller.py
RUN chown robot:robot /home/robot/service.sh
RUN chmod +x /home/robot/controller.py
RUN chmod +x /home/robot/service.sh

COPY ev3dev/roscontroller.service /etc/systemd/system/
RUN systemctl enable roscontroller.service



COPY ev3dev/ros_install.sh /root/
RUN chmod 766 /root/ros_install.sh
RUN /root/ros_install.sh
