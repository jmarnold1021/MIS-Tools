USE [ODS_production]
GO
/****** Object:  Table [dbo].[L56_DOD_SE]    Script Date: 5/12/2023 12:01:39 PM ******/
IF  EXISTS (SELECT * FROM sys.objects WHERE object_id = OBJECT_ID(N'[dbo].[L56_DOD_SE]') AND type in (N'U'))
DROP TABLE [dbo].[L56_DOD_SE]
GO
/****** Object:  Table [dbo].[L56_DOD_SE]    Script Date: 5/12/2023 12:01:39 PM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[L56_DOD_SE](
	[GI01] [varchar](3) NULL,
	[CCCCO_Assigned] [varchar](9) NOT NULL,
	[GI03] [varchar](3) NOT NULL,
	[SE01] [varchar](1) NULL,
	[SE02] [varchar](3) NULL,
	[SE03] [varchar](1) NULL,
	[SE04] [decimal](4, 2) NULL,
	[SE05] [varchar](1) NULL,
	[SE06] [varchar](3) NULL,
	[SE07] [varchar](1) NULL,
	[SE08] [varchar](1) NULL,
	[SE09] [varchar](1) NULL,
	[SE10] [varchar](1) NULL,
 CONSTRAINT [PK_DOD_SE_GI03_CCCCO_Assigned] PRIMARY KEY CLUSTERED 
(
	[GI03] DESC,
	[CCCCO_Assigned] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY]
GO
