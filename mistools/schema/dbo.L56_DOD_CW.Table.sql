USE [ODS_production]
GO
/****** Object:  Table [dbo].[L56_DOD_CW]    Script Date: 5/12/2023 12:01:39 PM ******/
IF  EXISTS (SELECT * FROM sys.objects WHERE object_id = OBJECT_ID(N'[dbo].[L56_DOD_CW]') AND type in (N'U'))
DROP TABLE [dbo].[L56_DOD_CW]
GO
/****** Object:  Table [dbo].[L56_DOD_CW]    Script Date: 5/12/2023 12:01:39 PM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[L56_DOD_CW](
	[GI01] [varchar](3) NULL,
	[CCCCO_Assigned] [varchar](9) NOT NULL,
	[GI03] [varchar](3) NOT NULL,
	[SC12] [varchar](1) NULL,
	[SC13] [varchar](6) NULL,
	[SC14] [varchar](8) NULL,
	[SC15] [varchar](8) NULL,
	[SC16] [int] NULL,
	[SC17] [decimal](4, 2) NULL,
 CONSTRAINT [PK_DOD_CW_GI03_CCCCO_Assigned] PRIMARY KEY CLUSTERED 
(
	[GI03] DESC,
	[CCCCO_Assigned] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY]
GO
